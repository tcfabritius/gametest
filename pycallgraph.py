from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

graphviz = GraphvizOutput()
graphviz.output_file = 'game_call_graph.png'

with PyCallGraph(output=graphviz):
    import game
    game.main()  # Replace with your main function or script