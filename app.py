def crear_grafica1_interactiva(data_grafica1):
    """Crea la gráfica 1 interactiva - CON CÁLCULOS CORREGIDOS"""
    if not data_grafica1 or data_grafica1.get("status") != "success":
        st.error("No se pudo cargar la gráfica 1: Datos inválidos o vacíos")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔄 Recargar datos", key="reload_graf1"):
                st.cache_data.clear()
                st.rerun()
        
        with col2:
            if st.button("🧪 Usar datos de ejemplo", key="use_example_graf1"):
                st.session_state["use_test_data"] = True
                st.rerun()
        return
    
    # Extraer datos del backend
    df_merge_fecha = pd.DataFrame(data_grafica1.get("tables", {}).get("df_merge_fecha", []))
    cand_raw = pd.DataFrame(data_grafica1.get("tables", {}).get("dias_validos", []))
    curve_raw = pd.DataFrame(data_grafica1.get("tables", {}).get("curva_15k", []))
    parameters = data_grafica1.get("parameters", {})
    summary = data_grafica1.get("results_summary", {})
    calc_data = data_grafica1.get("calc", {})
    
    # Parámetros CRÍTICOS (tomar del código original si no vienen)
    STEP = parameters.get("STEP", 15000)
    BREAK_X = parameters.get("BREAK_X", 80000.0)
    K = parameters.get("K", 0.28)
    IMPACT_DAYS = parameters.get("IMPACT_DAYS", 3)
    USE_IMPACT = parameters.get("USE_IMPACT", True)
    OPT_MIN_DAYS = parameters.get("OPT_MIN_DAYS", 3)
    OPT_CPS_TOL = parameters.get("OPT_CPS_TOL", 0.20)
    TARGET_FOLLOWERS = parameters.get("TARGET_FOLLOWERS", 1000)
    
    # COLUMNA RESULTADO CORRECTA (igual que original)
    RESULT_COL = "Seguidores_Impacto" if USE_IMPACT else "Neto_Diario_Real"
    
    # =========================================================================
    # CÁLCULOS CORREGIDOS - IGUAL AL CÓDIGO ORIGINAL
    # =========================================================================
    
    # Función para convertir números (igual que original)
    def to_num(v):
        if v is None or (isinstance(v, float) and np.isnan(v)):
            return np.nan
        if isinstance(v, (int, float, np.integer, np.floating)):
            return float(v)
        s = str(v).strip()
        if s == "":
            return np.nan
        s = s.replace("$", "").replace("COP", "").replace("cop", "").replace(" ", "")
        if "," in s and "." in s:
            if s.rfind(",") > s.rfind("."):
                s = s.replace(".", "").replace(",", ".")
            else:
                s = s.replace(",", "")
        else:
            if "," in s and "." not in s:
                s = s.replace(",", ".")
        try:
            return float(s)
        except Exception:
            return np.nan
    
    # Función de compresión X (igual que original)
    def x_warp(x):
        x = float(x)
        if x <= BREAK_X:
            return x
        return BREAK_X + (x - BREAK_X) * K
    
    # Función para encontrar punto óptimo (igual que original)
    def pick_optimal_point_seg_then_cps(df_curve, min_days=3, cps_tol=0.20):
        d = df_curve.copy()
        
        # Filtrar puntos válidos (igual que original)
        m = (
            d["Inversion_promedio"].notna() &
            d["Seguidores_promedio"].notna() &
            d["CPS_curva"].notna() &
            (d["Inversion_promedio"] > 0) &
            (d["Seguidores_promedio"] > 0) &
            (d["CPS_curva"] > 0) &
            (d["Dias"] >= int(min_days))
        )
        d = d[m].copy()
        
        if d.empty:
            # Si no hay puntos válidos, usar los primeros disponibles
            d = df_curve.copy()
            if d.empty:
                return None, 0, 0
        
        # Calcular CPS mínimo y máximo con tolerancia
        cps_min = float(d["CPS_curva"].min())
        cps_max = cps_min * (1.0 + float(cps_tol))
        
        # Filtrar por CPS dentro de la tolerancia
        d2 = d[d["CPS_curva"] <= cps_max].copy()
        if d2.empty:
            d2 = d.copy()
        
        # Ordenar: primero por más seguidores, luego por menor CPS, luego por menor inversión
        d2 = d2.sort_values(
            by=["Seguidores_promedio", "CPS_curva", "Inversion_promedio"],
            ascending=[False, True, True]
        )
        
        return d2.iloc[0].copy(), cps_min, cps_max
    
    # PROCESAR DATOS DE ENTRADA
    cand = cand_raw.copy()
    curve = curve_raw.copy()
    
    # Asegurar que tenemos las columnas necesarias en cand
    if cand.empty:
        st.error("No hay días válidos para calcular la gráfica")
        return
    
    # Asegurar columnas en cand
    required_cand_cols = ["Costo", RESULT_COL]
    for col in required_cand_cols:
        if col not in cand.columns:
            st.error(f"Falta columna requerida en días válidos: {col}")
            st.write("Columnas disponibles en cand:", cand.columns.tolist())
            return
    
    # Asegurar columnas en curve
    required_curve_cols = ["Inversion_promedio", "Seguidores_promedio", "CPS_curva", "Dias"]
    for col in required_curve_cols:
        if col not in curve.columns:
            st.error(f"Falta columna requerida en curva: {col}")
            st.write("Columnas disponibles en curve:", curve.columns.tolist())
            return
    
    # Calcular promedios reales desde cand (NO usar los que vienen)
    INV_mean = float(cand["Costo"].mean())
    SEG_mean = float(cand[RESULT_COL].mean())
    
    # Asegurar que la curva tenga CPS calculado correctamente
    if "CPS_curva" not in curve.columns or curve["CPS_curva"].isna().all():
        mask = (curve["Inversion_promedio"] > 0) & (curve["Seguidores_promedio"] > 0)
        curve.loc[mask, "CPS_curva"] = curve.loc[mask, "Inversion_promedio"] / curve.loc[mask, "Seguidores_promedio"]
    
    # Asegurar que la curva tenga días para meta
    if "Dias_para_meta" not in curve.columns:
        mask = curve["Seguidores_promedio"].notna() & (curve["Seguidores_promedio"] > 0)
        curve.loc[mask, "Dias_para_meta"] = TARGET_FOLLOWERS / curve.loc[mask, "Seguidores_promedio"]
    
    # Encontrar punto óptimo (CALCULARLO, no usar el que viene)
    opt, cps_min, cps_max = pick_optimal_point_seg_then_cps(
        curve, 
        min_days=OPT_MIN_DAYS, 
        cps_tol=OPT_CPS_TOL
    )
    
    if opt is not None:
        opt_x = float(opt["Inversion_promedio"])
        opt_y = float(opt["Seguidores_promedio"])
        opt_cps = float(opt["CPS_curva"])
        opt_dias_meta = float(opt.get("Dias_para_meta", 0))
        opt_dias = int(opt.get("Dias", 0))
    else:
        # Valores por defecto si no se puede calcular
        opt_x = 0
        opt_y = 0
        opt_cps = 0
        opt_dias_meta = 0
        opt_dias = 0
    
    # Aplicar compresión X a los datos
    cand["xw"] = cand["Costo"].apply(x_warp)
    curve["xw"] = curve["Inversion_promedio"].apply(x_warp)
    opt_xw = x_warp(opt_x) if opt_x > 0 else 0
    
    # Generar ticks del eje X (IGUAL AL ORIGINAL)
    cmin = float(cand["Costo"].min())
    cmax = float(cand["Costo"].max())
    start = float(np.floor(cmin / STEP) * STEP)
    end = float(np.ceil(cmax / STEP) * STEP) + STEP
    bins = np.arange(start, end + 1, STEP)
    
    # Filtrar bins visibles
    data_min = float(cand["Costo"].min())
    data_max = float(cand["Costo"].max())
    edge_ticks_real = np.unique(bins)
    edge_ticks_real = [x for x in edge_ticks_real if (x >= (np.floor(data_min/STEP)*STEP) - 1e-9 and x <= (np.ceil(data_max/STEP)*STEP) + 1e-9)]
    edge_ticks_w = [x_warp(x) for x in edge_ticks_real]
    edge_tick_labels = [formato_k_original(x) for x in edge_ticks_real]
    
    # Limitar número de ticks
    MAX_X_TICKS = 12
    stride = 1 if len(edge_ticks_real) <= MAX_X_TICKS else 2
    edge_ticks_real = edge_ticks_real[::stride]
    edge_ticks_w = edge_ticks_w[::stride]
    edge_tick_labels = edge_tick_labels[::stride]
    
    # =========================================================================
    # CREAR GRÁFICA (DISEÑO IDÉNTICO)
    # =========================================================================
    
    # Colores del gráfico original
    colors = {
        'fondo_figura': '#060913',
        'fondo_ejes': '#0b1020',
        'borde_ejes': '#334155',
        'texto': '#e0e7ff',
        'ticks': '#c7d2fe',
        'puntos_reales': '#60a5fa',
        'linea_curva': '#38bdf8',
        'puntos_curva': '#f59e0b',
        'linea_promedio': '#22d3ee',
        'punto_optimo': '#22c55e'
    }
    
    # Crear figura
    fig = go.Figure()
    
    # 1. Agregar líneas verticales para los bins
    for x_real in bins:
        if x_real >= (np.floor(data_min/STEP)*STEP) - 1e-9 and x_real <= (np.ceil(data_max/STEP)*STEP) + 1e-9:
            fig.add_vline(
                x=x_warp(x_real),
                line_width=1.0,
                line_dash="dash",
                line_color="#cbd5e1",
                opacity=0.18
            )
    
    # 2. Puntos de días reales
    fig.add_trace(go.Scatter(
        x=cand["xw"],
        y=cand[RESULT_COL],
        mode='markers',
        name='Días reales',
        marker=dict(
            size=6,
            color=colors['puntos_reales'],
            opacity=0.12,
            line=dict(width=0)
        ),
        hovertemplate='<b>📅 Día Real</b><br>Inversión: $%{x:,.0f}<br>Seguidores: %{y:,.0f}<extra></extra>'
    ))
    
    # 3. Línea de curva promedio
    fig.add_trace(go.Scatter(
        x=curve["xw"],
        y=curve["Seguidores_promedio"],
        mode='lines',
        name='Promedio esperado (por nivel inversión)',
        line=dict(color=colors['linea_curva'], width=2.8),
        opacity=0.95,
        hovertemplate='<b>📈 Curva promedio</b><br>Inversión: $%{x:,.0f}<br>Seguidores: %{y:,.0f}<br>CPS: $%{customdata:,.0f}<extra></extra>',
        customdata=curve["CPS_curva"]
    ))
    
    # 4. Puntos de la curva promedio con etiquetas
    for idx, row in curve.iterrows():
        # Solo mostrar etiquetas para puntos con datos válidos
        if pd.isna(row["Inversion_promedio"]) or pd.isna(row["Seguidores_promedio"]):
            continue
            
        # Crear etiqueta (formato original)
        dias_meta = row.get("Dias_para_meta", np.nan)
        label_text = (
            f"Inv {formato_numero_original(row['Inversion_promedio'])}<br>"
            f"SEG {formato_numero_original(row['Seguidores_promedio'])}<br>"
            f"CPS {formato_numero_original(row['CPS_curva'])}<br>"
            f"1000 SEG ~ {dias_meta:.1f} días<br>"
            f"Días {int(row['Dias'])}"
        )
        
        # Usar offset basado en la posición
        offset_idx = idx % len(LABEL_OFFSETS)
        dx, dy = LABEL_OFFSETS[offset_idx]
        
        # Añadir anotación
        fig.add_annotation(
            x=row["xw"],
            y=row["Seguidores_promedio"],
            text=label_text,
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=0.8,
            arrowcolor="#94a3b8",
            ax=dx,
            ay=dy,
            font=dict(size=8, color="white", family="Arial"),
            bgcolor="#0b1020",
            bordercolor="#334155",
            borderwidth=1,
            borderpad=4,
            opacity=0.90
        )
    
    # 5. Puntos naranjas de la curva (marcadores visibles)
    fig.add_trace(go.Scatter(
        x=curve["xw"],
        y=curve["Seguidores_promedio"],
        mode='markers',
        name='Puntos promedio (hover/click)',
        marker=dict(
            size=12,
            color=colors['puntos_curva'],
            opacity=0.98,
            line=dict(width=1, color='white')
        ),
        hovertemplate='<b>🎯 Punto curva</b><br>Inv: $%{x:,.0f}<br>SEG: %{y:,.0f}<br>CPS: $%{customdata:,.0f}<extra></extra>',
        customdata=curve["CPS_curva"],
        showlegend=True
    ))
    
    # 6. Punto óptimo (ESTRELLA VERDE) - solo si existe
    if opt_x > 0 and opt_y > 0:
        # Texto del punto óptimo
        opt_label_text = (
            f"Óptimo<br>"
            f"Inv {formato_numero_original(opt_x)}<br>"
            f"SEG {formato_numero_original(opt_y)}<br>"
            f"CPS {formato_numero_original(opt_cps)}<br>"
            f"1000 SEG ~ {opt_dias_meta:.1f} días<br>"
            f"CPS_min {formato_numero_original(cps_min)}<br>"
            f"CPS_max {formato_numero_original(cps_max)}"
        )
        
        # Añadir punto óptimo (ESTRELLA)
        fig.add_trace(go.Scatter(
            x=[opt_xw],
            y=[opt_y],
            mode='markers',
            name=f'Punto óptimo (max SEG dentro del mejor CPS, tol {int(OPT_CPS_TOL*100)}%)',
            marker=dict(
                size=25,
                color=colors['punto_optimo'],
                symbol='star',
                line=dict(width=1.8, color='white')
            ),
            hovertemplate='<b>⭐ PUNTO ÓPTIMO</b><br>Inversión: $%{x:,.0f}<br>Seguidores: %{y:,.0f}<br>CPS: $%{customdata:,.0f}<extra></extra>',
            customdata=[opt_cps]
        ))
        
        # Añadir etiqueta del punto óptimo
        opt_offset_idx = 0
        opt_dx, opt_dy = OPT_LABEL_OFFSETS[opt_offset_idx]
        
        fig.add_annotation(
            x=opt_xw,
            y=opt_y,
            text=opt_label_text,
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=0.8,
            arrowcolor="#94a3b8",
            ax=opt_dx,
            ay=opt_dy,
            font=dict(size=8, color="white", family="Arial"),
            bgcolor="#0b1020",
            bordercolor="#22c55e",
            borderwidth=1,
            borderpad=4,
            opacity=0.90
        )
    
    # 7. Líneas de promedio general
    # Línea horizontal de promedio SEG
    fig.add_hline(
        y=SEG_mean,
        line_dash="dot",
        line_color=colors['linea_promedio'],
        line_width=2.0,
        opacity=0.8,
        annotation_text=f"Promedio SEG = {formato_numero_original(SEG_mean)}",
        annotation_position="top right",
        annotation_font=dict(size=10, color=colors['linea_promedio']),
        annotation_bgcolor=colors['fondo_ejes']
    )
    
    # Línea vertical de promedio INV
    fig.add_vline(
        x=x_warp(INV_mean),
        line_dash="dot",
        line_color=colors['linea_promedio'],
        line_width=1.8,
        opacity=0.75,
        annotation_text=f"Promedio inversión = {formato_numero_original(INV_mean)}",
        annotation_position="top left",
        annotation_font=dict(size=10, color=colors['linea_promedio']),
        annotation_bgcolor=colors['fondo_ejes']
    )
    
    # Configurar layout
    fig.update_layout(
        height=700,
        plot_bgcolor=colors['fondo_ejes'],
        paper_bgcolor=colors['fondo_figura'],
        font=dict(color=colors['texto'], size=12, family="Arial"),
        title=dict(
            text=f"Inversión vs Seguidores (curva por niveles) — Hover/Click en puntos naranjas<br>"
                 f"<span style='font-size:14px; color:#94a3b8'>Impacto {IMPACT_DAYS}d | STEP ${STEP:,} | Compresión X: {BREAK_X/1000:.0f}k+ (K={K})</span>",
            font=dict(size=22, color='white', family="Arial Black"),
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        xaxis=dict(
            title="",
            gridcolor='rgba(255,255,255,0.1)',
            tickvals=edge_ticks_w,
            ticktext=edge_tick_labels,
            tickfont=dict(size=11, color=colors['ticks']),
            zeroline=False,
            showgrid=True,
            gridwidth=0.6
        ),
        yaxis=dict(
            title=f"Seguidores ({'Impacto' if USE_IMPACT else 'Neto'} {IMPACT_DAYS}d)",
            gridcolor='rgba(255,255,255,0.1)',
            tickformat=",",
            tickfont=dict(size=11, color=colors['ticks']),
            title_font=dict(size=13, color=colors['texto'])
        ),
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(11, 16, 32, 0.8)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1,
            font=dict(size=11, color=colors['texto'])
        ),
        margin=dict(l=60, r=40, t=120, b=60),
        showlegend=True
    )
    
    # Añadir grid horizontal
    fig.update_xaxes(showgrid=True, gridwidth=0.6, gridcolor='rgba(255,255,255,0.15)')
    fig.update_yaxes(showgrid=True, gridwidth=0.6, gridcolor='rgba(255,255,255,0.15)')
    
    # Mostrar gráfica
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
    
    # =========================================================================
    # INFORMACIÓN ADICIONAL CON CÁLCULOS CORRECTOS
    # =========================================================================
    
    # Mostrar información adicional en tarjetas
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "📊 Días válidos",
            f"{len(cand):,}",
            help="Total de días con inversión y seguidores positivos"
        )
    
    with col2:
        st.metric(
            "💰 Inv promedio",
            f"${INV_mean:,.0f}",
            help="Inversión promedio por día válido (calculado desde datos)"
        )
    
    with col3:
        st.metric(
            "👥 SEG promedio",
            f"{SEG_mean:,.0f}",
            help="Seguidores promedio por día válido (calculado desde datos)"
        )
    
    with col4:
        st.metric(
            "⭐ CPS mínimo",
            f"${cps_min:,.0f}",
            help="CPS mínimo encontrado en la curva"
        )
    
    with col5:
        st.metric(
            "🎯 CPS óptimo",
            f"${opt_cps:,.0f}",
            delta=f"Tol {int(OPT_CPS_TOL*100)}%",
            help=f"Costo por seguidor en el punto óptimo (tolerancia {int(OPT_CPS_TOL*100)}%)"
        )
    
    # Mostrar tabla de datos de la curva CON VALORES REALES
    with st.expander("📋 Ver datos detallados de la curva (rangos de inversión) - VALORES REALES"):
        display_curve = curve.copy()
        
        # Formatear como en el gráfico original
        display_curve["Inversion_promedio"] = display_curve["Inversion_promedio"].apply(
            lambda x: f"${x:,.0f}" if not pd.isna(x) else "N/A"
        )
        display_curve["Seguidores_promedio"] = display_curve["Seguidores_promedio"].apply(
            lambda x: f"{x:,.0f}" if not pd.isna(x) else "N/A"
        )
        display_curve["CPS_curva"] = display_curve["CPS_curva"].apply(
            lambda x: f"${x:,.0f}" if not pd.isna(x) else "N/A"
        )
        display_curve["Dias_para_meta"] = display_curve["Dias_para_meta"].apply(
            lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A"
        )
        
        # Renombrar columnas
        display_curve = display_curve.rename(columns={
            "Inversion_promedio": "💰 Inversión promedio",
            "Seguidores_promedio": "👥 Seguidores promedio",
            "CPS_curva": "📊 CPS",
            "Dias": "📅 Días en rango",
            "Dias_para_meta": "⏱️ 1000 SEG (días)"
        })
        
        st.dataframe(display_curve, use_container_width=True)
        
        # Mostrar información de parámetros
        st.info(f"""
        **Parámetros usados:**
        - STEP: ${STEP:,}
        - Impacto días: {IMPACT_DAYS}
        - Uso impacto: {USE_IMPACT}
        - Mínimo días para óptimo: {OPT_MIN_DAYS}
        - Tolerancia CPS: {int(OPT_CPS_TOL*100)}%
        - Compresión X: {BREAK_X/1000:.0f}k+ (K={K})
        """)
    
    # Botón para cambiar entre datos reales y de ejemplo
    st.markdown("---")
    col_switch1, col_switch2 = st.columns(2)
    
    with col_switch1:
        if st.session_state.get("use_test_data", False):
            if st.button("🔄 Cambiar a datos reales", key="switch_to_real"):
                st.session_state["use_test_data"] = False
                st.rerun()
        else:
            if st.button("🧪 Usar datos de ejemplo", key="switch_to_example"):
                st.session_state["use_test_data"] = True
                st.rerun()
    
    with col_switch2:
        if st.button("📊 Ver datos crudos y cálculos", key="show_raw_data"):
            with st.expander("📁 Datos crudos y cálculos detallados"):
                st.write("**Parámetros usados:**", parameters)
                st.write("**Resumen del backend:**", summary)
                st.write("**Cálculos realizados:**", {
                    "INV_mean": INV_mean,
                    "SEG_mean": SEG_mean,
                    "cps_min": cps_min,
                    "cps_max": cps_max,
                    "opt_x": opt_x,
                    "opt_y": opt_y,
                    "opt_cps": opt_cps,
                    "opt_dias_meta": opt_dias_meta,
                    "opt_dias": opt_dias
                })
                
                st.write("**Días válidos (primeras 10 filas):**")
                st.dataframe(cand[["Costo", RESULT_COL]].head(10))
                
                st.write("**Curva completa con cálculos:**")
                st.dataframe(curve)
                
                # Mostrar advertencia si los datos parecen incorrectos
                if INV_mean > 200000:
                    st.warning("⚠️ **ADVERTENCIA:** La inversión promedio parece muy alta. Verificar los datos de entrada.")
                if len(cand) < 5:
                    st.warning("⚠️ **ADVERTENCIA:** Muy pocos días válidos. Los resultados pueden no ser confiables.")
