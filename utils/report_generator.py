import pandas as pd
import os
import json

def generar_reporte_html(df_users: pd.DataFrame, df_products: pd.DataFrame, output_path="reports/reporte.html"):
    """
    Genera un dashboard HTML bonito e interactivo con tablas, gráficos y estadísticas.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # === 📊 Calcular estadísticas ===
    total_users = len(df_users)
    total_products = len(df_products)
    avg_price = round(df_products["price"].mean(), 2) if "price" in df_products else 0
    top_user = df_users.loc[df_users["puntos"].idxmax(), "name"] if not df_users.empty else "N/A"
    top_points = df_users["puntos"].max() if not df_users.empty else 0

    # === 📈 Datos para los gráficos (Chart.js) ===
    top_users = df_users.nlargest(5, "puntos")[["name", "puntos"]].to_dict(orient="records")
    price_values = df_products["price"].tolist()

    # ✂️ Limitar descripción larga
    if "description" in df_products.columns:
        df_products["description"] = df_products["description"].apply(
            lambda x: f'<span title="{x}">{x[:100]}{"..." if len(x) > 100 else ""}</span>' if isinstance(x, str) else x
        )

    # === 📄 HTML completo ===
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard Game Connect</title>

        <!-- CSS -->
        <link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

        <!-- JS -->
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f6f8;
                padding: 30px;
            }}
            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 40px;
            }}
            .card {{
                border: none;
                border-radius: 15px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .table-section {{
                margin-top: 40px;
            }}
            table {{
                width: 100%;
                background-color: white;
                word-wrap: break-word;
            }}
            canvas {{
                background: #fff;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            /* Tabla de productos */
            #tabla_productos {{
                border-collapse: separate;
                border-spacing: 0 8px;
                table-layout: fixed;
                word-wrap: break-word;
            }}
            #tabla_productos thead {{
                background-color: #2c3e50;
                color: #fff;
            }}
            #tabla_productos tbody tr {{
                background-color: #ffffff;
                transition: all 0.2s ease;
            }}
            #tabla_productos tbody tr:hover {{
                background-color: #f0f7ff;
                transform: scale(1.01);
            }}
            #tabla_productos td, #tabla_productos th {{
                padding: 12px 16px;
                border: none;
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }}
            #tabla_productos td span {{
                cursor: help;
                display: inline-block;
                max-width: 350px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
        </style>
    </head>
    <body>
        <h1>🎮 Dashboard Game Connect</h1>

        <!-- Tarjetas de resumen -->
        <div class="container text-center mb-5">
            <div class="row g-4">
                <div class="col-md-3">
                    <div class="card p-3">
                        <h5>Total Usuarios</h5>
                        <h2>{total_users}</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card p-3">
                        <h5>Total Productos</h5>
                        <h2>{total_products}</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card p-3">
                        <h5>Precio Promedio</h5>
                        <h2>${avg_price}</h2>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card p-3">
                        <h5>Top Usuario</h5>
                        <h2>{top_user}</h2>
                        <p>{top_points} pts</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Gráficos -->
        <div class="container mb-5">
            <div class="row g-4">
                <div class="col-md-6">
                    <h4>🏆 Top 5 Usuarios por Puntos</h4>
                    <canvas id="chartUsers"></canvas>
                </div>
                <div class="col-md-6">
                    <h4>💰 Distribución de Precios</h4>
                    <canvas id="chartPrices"></canvas>
                </div>
            </div>
        </div>

        <!-- Tablas -->
        <div class="container table-section">
            <h3>👥 Usuarios</h3>
            {df_users.to_html(index=False, classes="display table table-striped", table_id="tabla_usuarios")}
        </div>

        <div class="container table-section">
            <h3>🛍️ Productos</h3>
            <div class="card p-4 shadow-sm" style="background: white; border-radius: 15px;">
                <div class="table-responsive">
                    {df_products.to_html(
                        index=False,
                        classes="table table-hover align-middle mb-0",
                        table_id="tabla_productos",
                        escape=False  # 👈 Permite HTML en descripción
                    )}
                </div>
            </div>
        </div>

        <!-- Scripts -->
        <script>
            // Inicializar DataTables
            $(document).ready(function() {{
                $('#tabla_usuarios').DataTable({{ pageLength: 5, language: {{ search: "Buscar usuario:" }} }});
                $('#tabla_productos').DataTable({{ pageLength: 5, language: {{ search: "Buscar producto:" }} }});
            }});

            // Gráfico de usuarios
            const topUsers = {json.dumps(top_users)};
            const ctxUsers = document.getElementById('chartUsers').getContext('2d');
            new Chart(ctxUsers, {{
                type: 'bar',
                data: {{
                    labels: topUsers.map(u => u.name),
                    datasets: [{{
                        label: 'Puntos',
                        data: topUsers.map(u => u.puntos),
                        backgroundColor: '#3498db'
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{ beginAtZero: true }}
                    }}
                }}
            }});

            // Gráfico de precios
            const prices = {json.dumps(price_values)};
            const ctxPrices = document.getElementById('chartPrices').getContext('2d');
            new Chart(ctxPrices, {{
                type: 'line',
                data: {{
                    labels: prices.map((_, i) => i + 1),
                    datasets: [{{
                        label: 'Precio',
                        data: prices,
                        borderColor: '#2ecc71',
                        fill: false
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{ beginAtZero: true }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """

    # Guardar archivo
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Reporte visual generado correctamente en: {os.path.abspath(output_path)}")
