'''
VISUALIZADOR

Genera los archivos HTML para visualizar las rutas entre dos prefijos y la información de un AS
'''

import json


def generar_html_rutas(prefijo_a, origenes_a, prefijo_b, origenes_b, rutas):
    # Nodos: cada AS que aparece en alguna ruta. Aristas: cada par de AS seguidos en una ruta
    nodos = set()
    aristas = set()
    for ruta in rutas:
        for i in range(len(ruta)):
            nodos.add(ruta[i])
            if i > 0:
                aristas.add((ruta[i - 1], ruta[i]))

    lista_nodos = []
    for numero_as in nodos:
        nodo = {"id": numero_as, "label": str(numero_as)}
        if numero_as in origenes_a:
            nodo["color"] = {"background": "#1864ab", "border": "#4dabf7"}
        elif numero_as in origenes_b:
            nodo["color"] = {"background": "#66d9e8", "border": "#99e9f2"}
            nodo["font"] = {"color": "#1e1e1e"}
        lista_nodos.append(nodo)

    lista_aristas = []
    for a, b in aristas:
        lista_aristas.append({"from": a, "to": b})

    html = PLANTILLA_RUTAS
    html = html.replace("PREFIJO_A", prefijo_a)
    html = html.replace("PREFIJO_B", prefijo_b)
    html = html.replace("ORIGENES_A", ", ".join(str(x) for x in origenes_a))
    html = html.replace("ORIGENES_B", ", ".join(str(x) for x in origenes_b))
    html = html.replace("TOTAL_RUTAS", str(len(rutas)))
    html = html.replace("LISTA_NODOS", json.dumps(lista_nodos))
    html = html.replace("LISTA_ARISTAS", json.dumps(lista_aristas))

    with open("visualizador_rutas.html", "w", encoding="utf-8") as archivo:
        archivo.write(html)


def generar_html_tabla_as(numero_as, filas):
    # Una fila de la tabla por cada prefijo conocido por el AS
    texto_filas = ""
    for fila in filas:
        texto_filas += f"<tr><td>{fila['ip']}</td><td>{fila['prefijo']}</td><td>{fila['path']}</td></tr>\n"

    html = PLANTILLA_TABLA
    html = html.replace("NUMERO_AS", str(numero_as))
    html = html.replace("TOTAL_FILAS", str(len(filas)))
    html = html.replace("FILAS_TABLA", texto_filas)

    with open("reporte_as.html", "w", encoding="utf-8") as archivo:
        archivo.write(html)


PLANTILLA_RUTAS = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Rutas entre PREFIJO_A y PREFIJO_B</title>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald&display=swap">
<style>
  body { font-family: Oswald, Arial; background: #1e1e1e; color: #eeeeee; }
  h2, p { text-align: center; }
  h2 { font-size: 40px; }
  p { font-size: 24px; }
  .origen-a { color: #4dabf7; font-weight: bold; }
  .origen-b { color: #66d9e8; font-weight: bold; }
  #grafo { width: 100%; height: 600px; border: 1px solid #444444; }
</style>
</head>
<body>
<h2>Rutas entre PREFIJO_A y PREFIJO_B</h2>
<p>Origen de A: <span class="origen-a">ORIGENES_A</span>. Origen de B: <span class="origen-b">ORIGENES_B</span>. Total de rutas: TOTAL_RUTAS.</p>
<div id="grafo"></div>
<script>
  var nodos = new vis.DataSet(LISTA_NODOS);
  var aristas = new vis.DataSet(LISTA_ARISTAS);
  var opciones = {
    nodes: {
      shape: "circle",
      borderWidth: 2,
      widthConstraint: { minimum: 70 },
      color: { background: "#2b2b2b", border: "#555555" },
      font: { face: "Oswald", size: 16, color: "#eeeeee" }
    },
    edges: { arrows: "to", color: "#aaaaaa", smooth: false },
    physics: { barnesHut: { avoidOverlap: 1 } }
  };
  new vis.Network(document.getElementById("grafo"), { nodes: nodos, edges: aristas }, opciones);
</script>
</body>
</html>
'''

PLANTILLA_TABLA = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AS NUMERO_AS</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald&display=swap">
<style>
  body { font-family: Oswald, Arial; background: #1e1e1e; color: #eeeeee; }
  h2, p { text-align: center; }
  h2 { font-size: 40px; }
  p { font-size: 24px; }
  table { border-collapse: collapse; margin: auto; }
  th, td { border: 1px solid #444444; padding: 6px 10px; text-align: left; }
  th { background: #1864ab; }
</style>
</head>
<body>
<h2>Información del AS NUMERO_AS</h2>
<p>Total de prefijos: TOTAL_FILAS</p>
<table>
<tr><th>IP del peer</th><th>Prefijo</th><th>AS Path</th></tr>
FILAS_TABLA
</table>
</body>
</html>
'''