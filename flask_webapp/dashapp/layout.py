# html_layout = '''
#                 {% extends "layout.html" %}
#                 {% block content %}
#                     <h1>Stock Screener</h1>
#                     <body>
#                         Stock screener will go here. Add from Dash App.
#                         <a href="/screener/"><i class="fas fa-chart-line"></i> Embdedded Plotly Dash</a>
#                     {%app_entry%}
#                     <footer>
#                     {%config%}
#                     {%scripts%}
#                     {%renderer%}
#                     </footer>

#                     </body>
#                 {% endblock content %}
                
#             '''