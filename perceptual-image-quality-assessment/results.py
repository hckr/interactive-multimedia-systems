import json
import matplotlib.pyplot as plt


def main():
    results = json.load(open('survey-results.json'))
    results2 = list(map(lambda x: list(zip(*sorted(x))), results))
    labels = results2[0][0]
    assessments = map(lambda x: x[1], results2)
    for a in assessments:
        plt.plot(labels, a, '-*')
    plt.xticks(labels)
    plt.yticks([1, 2, 3, 4, 5])
    plt.show()


if __name__ == "__main__":
    main()
