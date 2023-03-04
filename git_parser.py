# import gitlab
# import matplotlib.pyplot as plt
#
# # def parse_git():
# gl = gitlab.Gitlab('https://github.com/', private_token='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')
#
# # gl = gitlab.Gitlab('https://gitlab.com/', oauth_token='TwZ3tsiyHDPm1za5WYNd')
# gl.auth()
# test = gl.user
# print(test)

from github import Github
import networkx as nx
import matplotlib.pyplot as plt

graph = nx.DiGraph()

g = Github('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')

user = g.get_user('Dannyel9313')

repos = user.get_repos()
for repo in repos:

    # pulls = repo.get_pulls()
    # merges = [pull for pull in pulls if pull.merged]
    # print(merges)
    # print(repo.name)
    if repo.name == 'Algorithm':

        branches = repo.get_branches()
        for branch in branches:
            print(branch.name)

        commits = repo.get_commits();
        for commit in commits:
            print(commit.sha)
            graph.add_node(commit.sha)
            for parent in commit.parents:
                print(parent.sha)
                graph.add_edge(parent.sha,commit.sha)

pos = nx.spring_layout(graph, k=0.3)

nx.draw(graph, pos, with_labels=True, node_size=1000, font_size=8, node_color='#008fd5', edge_color='#e6e6e6')

plt.show()



