import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import csv

path_image_folder = 'C:\image_example'
cluster_csv = 'cluster_data.csv'

df = pd.read_csv(cluster_csv)

def add_csv_cluster_tx(cluster_data_tx:list):
    csv_cluster_tx = 'cluster_tx.csv'
    file_exists = os.path.isfile(csv_cluster_tx)
    fieldnames = ['cluster', 'hash', 'from_chain', 'to_chain', 'from_wallet', 'to_wallet']
    with open(csv_cluster_tx, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists or os.path.getsize(csv_cluster_tx) == 0:
            writer.writeheader()
        for idx, row in enumerate(cluster_data_tx):
            writer.writerow(row)
            
def add_csv_cluster(cluster_data:list):
    csv_cluster = 'cluster.csv'
    file_exists = os.path.isfile(csv_cluster)
    fieldnames = ['cluster', 'name', 'wallet']
    with open(csv_cluster, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists or os.path.getsize(csv_cluster) == 0:
            writer.writeheader()
        for idx, row in enumerate(cluster_data):
            writer.writerow(row)
        

G = nx.from_pandas_edgelist(df, 'from_wallet', 'to_wallet')

def draw_clusters(G):
    cluster_count = 1
    clusters = list(nx.connected_components(G))
    for i, cluster in enumerate(clusters):
        print(cluster_count)
        cluster_data = list()
        cluster_data_tx = list()
        if len(cluster) >= 6:
            cluster_name = f"Cluster {cluster_count}({len(cluster)})"
            plt.figure(figsize=(10, 5))  
            plt.title(f"Cluster (wallets: {len(cluster)})")
            node_labels={}
            w_num = 0
            cluster_records = df[(df['from_wallet'].isin(cluster)) | (df['to_wallet'].isin(cluster))]
            for index, transaction in cluster_records.iterrows():
                cluster_data_tx_dict = dict()
                cluster_data_tx_dict.update(
                    {
                        'cluster': cluster_name,
                        'hash' : transaction['hash'],
                        'from_chain' : transaction['from_chain'],
                        'to_chain' : transaction['to_chain'],
                        'from_wallet' : transaction['from_wallet'],
                        'to_wallet' : transaction['to_wallet'],
                    }
                )
                cluster_data_tx.append(cluster_data_tx_dict)
            for indexnode_node, node in enumerate(cluster):
                w_num += 1
                cluster_data_dict = dict()
                cluster_data_dict.update(
                    {
                        'cluster': cluster_name,
                        'name': f'W{w_num}',
                        'wallet': node,
                    }
                )
                cluster_data.append(cluster_data_dict)
                print(f'W{w_num} : {node}')
                node_labels.update({node:f'W{w_num}'})
            add_csv_cluster(cluster_data=cluster_data)
            add_csv_cluster_tx(cluster_data_tx=cluster_data_tx)

            pos = nx.spring_layout(G.subgraph(cluster),k=0.1)  
            nx.draw(G.subgraph(cluster), pos, with_labels=True, labels=node_labels, node_color='skyblue', node_size=200, font_size=6, font_weight='bold', arrows=True)
            plt.savefig(fr'{path_image_folder}\{cluster_name}.png')
            plt.close()
            cluster_count +=1 
            
draw_clusters(G)

