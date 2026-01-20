"""
Network Structure Module
For studying the effect of group structure on game outcomes

4 Network Topologies:
1. Complete - Every node connects to all others
2. Ring - Nodes form a circle, connect to neighbors only
3. Small World - High clustering + short path length
4. Scale Free - Power-law degree distribution, hub nodes exist
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class NetworkMetrics:
    """Network metrics data class"""
    n_nodes: int
    n_edges: int
    density: float
    avg_degree: float
    avg_clustering: float
    avg_path_length: float

    def to_dict(self) -> dict:
        return {
            'nodes': self.n_nodes,
            'edges': self.n_edges,
            'density': round(self.density, 4),
            'avg_degree': round(self.avg_degree, 2),
            'clustering': round(self.avg_clustering, 4),
            'path_length': round(self.avg_path_length, 2) if self.avg_path_length != float('inf') else 'inf'
        }


class NetworkGenerator:
    """
    Network Structure Generator

    Supports 4 classic network topologies:
    1. Complete - Full mesh, everyone knows everyone
    2. Ring - Regular lattice in circle form
    3. Small World (Watts-Strogatz) - High clustering + short paths
    4. Scale Free (Barabasi-Albert) - Hub nodes, power-law distribution
    """

    @staticmethod
    def complete(n: int) -> nx.Graph:
        """
        Complete Graph
        - Every pair of nodes is connected
        - Fastest information spread
        - Edges = n(n-1)/2
        """
        G = nx.complete_graph(n)
        G.graph['type'] = 'complete'
        G.graph['name'] = 'Complete'
        return G

    @staticmethod
    def ring(n: int, k: int = 2) -> nx.Graph:
        """
        Ring Network (Regular Lattice)

        Args:
            n: number of nodes
            k: neighbors on each side (total neighbors = 2k)

        Features:
        - High clustering coefficient
        - Long average path length
        - Strong locality
        """
        G = nx.watts_strogatz_graph(n, k*2, 0)  # p=0 gives regular ring
        G.graph['type'] = 'ring'
        G.graph['name'] = 'Ring'
        return G

    @staticmethod
    def small_world(n: int, k: int = 4, p: float = 0.1,
                    seed: Optional[int] = None) -> nx.Graph:
        """
        Small World Network (Watts-Strogatz Model)

        Args:
            n: number of nodes
            k: each node connects to k nearest neighbors (must be even)
            p: rewiring probability (0=ring, 1=random)

        Features:
        - High clustering (like regular network)
        - Short average path (like random network)
        - "Six degrees of separation" phenomenon
        """
        G = nx.watts_strogatz_graph(n, k, p, seed=seed)
        G.graph['type'] = 'small_world'
        G.graph['name'] = 'Small World'
        G.graph['params'] = {'k': k, 'p': p}
        return G

    @staticmethod
    def scale_free(n: int, m: int = 2,
                   seed: Optional[int] = None) -> nx.Graph:
        """
        Scale-Free Network (Barabasi-Albert Model)

        Args:
            n: number of nodes
            m: edges to attach from new node

        Features:
        - Few hub nodes with many connections
        - Degree distribution follows power law P(k) ~ k^(-gamma)
        - Robust to random failure, vulnerable to targeted attack
        """
        G = nx.barabasi_albert_graph(n, m, seed=seed)
        G.graph['type'] = 'scale_free'
        G.graph['name'] = 'Scale Free'
        G.graph['params'] = {'m': m}
        return G

    @staticmethod
    def random(n: int, p: float = 0.1,
               seed: Optional[int] = None) -> nx.Graph:
        """
        Random Network (Erdos-Renyi Model)

        Args:
            n: number of nodes
            p: probability of edge between any pair

        Features:
        - Poisson degree distribution
        - Low clustering coefficient
        - Used as baseline/control
        """
        G = nx.erdos_renyi_graph(n, p, seed=seed)
        G.graph['type'] = 'random'
        G.graph['name'] = 'Random'
        G.graph['params'] = {'p': p}
        return G

    @classmethod
    def create(cls, network_type: str, n: int, **kwargs) -> nx.Graph:
        """
        Unified creation interface

        Args:
            network_type: 'complete', 'ring', 'small_world', 'scale_free', 'random'
            n: number of nodes
            **kwargs: additional parameters
        """
        generators = {
            'complete': cls.complete,
            'ring': cls.ring,
            'small_world': cls.small_world,
            'scale_free': cls.scale_free,
            'random': cls.random
        }

        if network_type not in generators:
            available = ', '.join(generators.keys())
            raise ValueError(f"Unknown network type: {network_type}. Available: {available}")

        return generators[network_type](n, **kwargs)

    @staticmethod
    def get_available_types() -> List[str]:
        """Get all available network types"""
        return ['complete', 'ring', 'small_world', 'scale_free', 'random']


class NetworkAnalyzer:
    """Network analysis tools"""

    @staticmethod
    def compute_metrics(G: nx.Graph) -> NetworkMetrics:
        """
        Compute network metrics

        Returns:
            NetworkMetrics dataclass
        """
        n_nodes = G.number_of_nodes()
        n_edges = G.number_of_edges()

        # Density = actual edges / max possible edges
        density = nx.density(G)

        # Average degree
        degrees = dict(G.degree())
        avg_degree = sum(degrees.values()) / n_nodes if n_nodes > 0 else 0

        # Average clustering coefficient
        avg_clustering = nx.average_clustering(G)

        # Average path length (requires connected graph)
        if nx.is_connected(G):
            avg_path_length = nx.average_shortest_path_length(G)
        else:
            # Use largest connected component
            largest_cc = max(nx.connected_components(G), key=len)
            if len(largest_cc) > 1:
                subgraph = G.subgraph(largest_cc)
                avg_path_length = nx.average_shortest_path_length(subgraph)
            else:
                avg_path_length = float('inf')

        return NetworkMetrics(
            n_nodes=n_nodes,
            n_edges=n_edges,
            density=density,
            avg_degree=avg_degree,
            avg_clustering=avg_clustering,
            avg_path_length=avg_path_length
        )

    @staticmethod
    def compare_networks(networks: Dict[str, nx.Graph]) -> Dict[str, dict]:
        """
        Compare metrics of multiple networks

        Args:
            networks: {name: graph} dictionary

        Returns:
            {name: metrics_dict} dictionary
        """
        results = {}
        for name, G in networks.items():
            metrics = NetworkAnalyzer.compute_metrics(G)
            results[name] = metrics.to_dict()
        return results

    @staticmethod
    def get_degree_distribution(G: nx.Graph) -> Dict[int, int]:
        """Get degree distribution"""
        degrees = [d for n, d in G.degree()]
        distribution = {}
        for d in degrees:
            distribution[d] = distribution.get(d, 0) + 1
        return dict(sorted(distribution.items()))


class NetworkVisualizer:
    """Network visualization tools"""

    @staticmethod
    def plot_network(G: nx.Graph, title: str = None,
                     ax=None, node_color='skyblue',
                     show_labels: bool = False) -> None:
        """
        Plot a single network

        Args:
            G: NetworkX graph
            title: plot title
            ax: matplotlib axes
            node_color: color of nodes
            show_labels: whether to show node labels
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 8))

        # Layout
        if G.graph.get('type') == 'ring':
            pos = nx.circular_layout(G)
        else:
            pos = nx.spring_layout(G, seed=42, k=2/np.sqrt(G.number_of_nodes()))

        # Node size based on degree
        degrees = dict(G.degree())
        max_degree = max(degrees.values()) if degrees else 1
        node_sizes = [100 + (degrees[node] / max_degree) * 300 for node in G.nodes()]

        # Draw
        nx.draw(G, pos, ax=ax,
                node_color=node_color,
                node_size=node_sizes,
                edge_color='gray',
                alpha=0.8,
                with_labels=show_labels,
                font_size=8)

        # Title
        if title is None:
            title = G.graph.get('name', 'Network')
        metrics = NetworkAnalyzer.compute_metrics(G)
        ax.set_title(f"{title}\n(N={metrics.n_nodes}, E={metrics.n_edges}, "
                    f"C={metrics.avg_clustering:.3f})")

    @staticmethod
    def plot_comparison(networks: Dict[str, nx.Graph],
                        save_path: Optional[str] = None) -> None:
        """
        Compare multiple networks side by side

        Args:
            networks: {name: graph} dictionary
            save_path: path to save figure (optional)
        """
        n = len(networks)
        fig, axes = plt.subplots(1, n, figsize=(5*n, 5))

        if n == 1:
            axes = [axes]

        colors = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6', '#f39c12']

        for ax, (name, G), color in zip(axes, networks.items(), colors):
            NetworkVisualizer.plot_network(G, title=name, ax=ax, node_color=color)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Figure saved: {save_path}")

        plt.show()

    @staticmethod
    def plot_degree_distribution(G: nx.Graph, title: str = None,
                                 ax=None) -> None:
        """Plot degree distribution histogram"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))

        degrees = [d for n, d in G.degree()]

        ax.hist(degrees, bins=range(max(degrees)+2),
                color='steelblue', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Degree')
        ax.set_ylabel('Frequency')
        ax.set_title(title or f'Degree Distribution - {G.graph.get("name", "Network")}')
        ax.grid(True, alpha=0.3)


# ============ Test Code ============
if __name__ == "__main__":
    print("=" * 60)
    print("Network Structure Module Test")
    print("=" * 60)

    n = 30  # Number of nodes

    # 1. Create different network types
    print("\n[Test 1] Creating networks...")
    networks = {
        'Complete': NetworkGenerator.complete(n),
        'Ring': NetworkGenerator.ring(n, k=2),
        'Small World': NetworkGenerator.small_world(n, k=4, p=0.1, seed=42),
        'Scale Free': NetworkGenerator.scale_free(n, m=2, seed=42)
    }

    for name, G in networks.items():
        print(f"  OK {name}: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # 2. Compute network metrics
    print("\n[Test 2] Network metrics comparison...")
    comparison = NetworkAnalyzer.compare_networks(networks)

    # Print table
    print("\n  " + "-" * 75)
    print(f"  {'Network':<12} {'Nodes':<7} {'Edges':<8} {'Density':<9} {'Avg Deg':<9} {'Cluster':<10} {'Path Len':<10}")
    print("  " + "-" * 75)

    for name, metrics in comparison.items():
        print(f"  {name:<12} {metrics['nodes']:<7} {metrics['edges']:<8} "
              f"{metrics['density']:<9} {metrics['avg_degree']:<9} "
              f"{metrics['clustering']:<10} {metrics['path_length']:<10}")

    # 3. Test factory method
    print("\n[Test 3] Using factory method...")
    G = NetworkGenerator.create('small_world', n=50, k=6, p=0.2)
    print(f"  Created: {G.graph}")

    # 4. Get neighbors (for game pairing)
    print("\n[Test 4] Getting node neighbors...")
    G = NetworkGenerator.small_world(10, k=4, p=0.1, seed=42)
    for node in range(3):
        neighbors = list(G.neighbors(node))
        print(f"  Node {node} neighbors: {neighbors}")

    # 5. Visualization
    print("\n[Test 5] Network visualization...")
    try:
        NetworkVisualizer.plot_comparison(networks, save_path='network_comparison.png')
        print("  OK Visualization complete")
    except Exception as e:
        print(f"  (Visualization skipped: {e})")

    print("\n" + "=" * 60)
    print("Network module test complete!")
    print("=" * 60)
