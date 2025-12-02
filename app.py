from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import json
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "service": "TikTok Data Processor API",
        "version": "1.0",
        "endpoints": {
            "/process": "POST - Procesar datos scrapeados",
            "/health": "GET - Verificar estado"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/process', methods=['POST'])
def process_data():
    """Procesar datos scrapeados enviados desde Streamlit"""
    try:
        data = request.get_json()
        videos_data = data.get('videos', [])
        
        if not videos_data:
            return jsonify({
                "error": "No hay datos para procesar",
                "message": "Envía datos de videos scrapeados"
            }), 400
        
        # Crear DataFrame
        df = pd.DataFrame(videos_data)
        
        # Convertir métricas a numéricas
        def convert_metric(val):
            if isinstance(val, (int, float)):
                return val
            val_str = str(val).replace(',', '').replace('K', '000')
            try:
                return int(float(val_str))
            except:
                return 0
        
        if 'visualizaciones' in df.columns:
            df['visualizaciones_num'] = df['visualizaciones'].apply(convert_metric)
        if 'me_gusta' in df.columns:
            df['me_gusta_num'] = df['me_gusta'].apply(convert_metric)
        if 'comentarios' in df.columns:
            df['comentarios_num'] = df['comentarios'].apply(convert_metric)
        
        # Calcular engagement
        if 'visualizaciones_num' in df.columns and 'me_gusta_num' in df.columns and 'comentarios_num' in df.columns:
            df['engagement_rate'] = ((df['me_gusta_num'] + df['comentarios_num']) / 
                                   df['visualizaciones_num'].replace(0, 1) * 100).round(2)
        
        # Ordenar por fecha
        if 'fecha_publicacion' in df.columns:
            try:
                df = df.sort_values('fecha_publicacion', ascending=False)
            except:
                pass
        
        # Convertir a lista de diccionarios
        processed_data = df.to_dict('records')
        
        # Crear CSV temporal
        csv_buffer = tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False, encoding='utf-8')
        df.to_csv(csv_buffer, index=False)
        csv_buffer.flush()
        csv_path = csv_buffer.name
        
        return jsonify({
            "status": "success",
            "count": len(processed_data),
            "data": processed_data,
            "csv_path": csv_path,
            "analytics": {
                "total_videos": len(df),
                "total_views": int(df['visualizaciones_num'].sum()),
                "total_likes": int(df['me_gusta_num'].sum()),
                "total_comments": int(df['comentarios_num'].sum()),
                "avg_engagement": float(df['engagement_rate'].mean()) if 'engagement_rate' in df.columns else 0
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/download')
def download_csv():
    try:
        csv_path = request.args.get('path', '')
        if not csv_path or not os.path.exists(csv_path):
            return jsonify({"error": "Archivo no encontrado"}), 404
        
        return send_file(
            csv_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'tiktok_metrics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
