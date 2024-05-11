import csv
import os

def process_scores(name, attempts, scores):
    """
    Process and store student scores.

    Args:
        name (str): Student's name.
        attempts (int): Number of attempts made.
        scores (list): List of scores.

    Returns:
        tuple: Message indicating success/failure, boolean flag.
    """
    if len(scores) > 4:
        return "Only up to 4 scores are allowed.", False

    scores = [int(score) if score.isdigit() and 0 <= int(score) <= 100 else 0 for score in scores]
    scores += [0] * (4 - len(scores))

    filename = 'grades.csv'
    fieldnames = ['Name', 'Score 1', 'Score 2', 'Score 3', 'Score 4', 'Final']
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        valid_scores = [score for score in scores if score != 0]
        final_score_formatted = "{:.2f}".format(sum(valid_scores) / len(valid_scores)) if valid_scores else "0.00"

        row = {'Name': name, 'Score 1': scores[0], 'Score 2': scores[1], 'Score 3': scores[2], 'Score 4': scores[3],
               'Final': final_score_formatted}

        writer.writerow(row)

    return "Scores submitted successfully.", True
