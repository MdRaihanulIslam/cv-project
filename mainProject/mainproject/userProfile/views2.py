import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def fetchAndSaveToFile(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    submissions_table = soup.find('table', class_='table -submissions -emphasis')
    submissions = []
    if submissions_table:
        for row in submissions_table.find('tbody').find_all('tr')[0:]:
            cells = row.find_all('td')
            if len(cells) >= 6:
                submission = {
                    'problem': cells[3].a.get("href").split('/')[-1],
                    'verdict': cells[5].text.strip()[0]  # 'A' for Accepted, others for Wrong
                }
                submissions.append(submission)
    return submissions

def getProblemTags(problem_id):
    problemUrl = "https://toph.co/p/" + problem_id
    r = requests.get(problemUrl)
    soup = BeautifulSoup(r.text, 'html.parser')
    flair_divs = soup.find_all('div', class_='flair')
    tags = []
    if len(flair_divs) > 1:
        tag_links = flair_divs[1].select('span.text a')
        tags = [tag.text for tag in tag_links]
    return tags

def analyzeUserSubmissions(acId):
    value = 0
    tag_problem_accuracies = defaultdict(list)
    processed_problems = {}

    while True:
        if value>200:
            break
        url = f"https://toph.co/submissions/filter?author={acId}&start={value}"
        submissions = fetchAndSaveToFile(url)
        if not submissions:
            break
        
        # Track how many attempts and accepted submissions per problem
        problem_attempts = defaultdict(lambda: {'attempts': 0, 'accepted': 0})

        for sub in submissions:
            problem_id = sub['problem']
            verdict = sub['verdict']
            
            # Track attempts and accepted for each problem
            problem_attempts[problem_id]['attempts'] += 1
            if verdict == 'A':
                problem_attempts[problem_id]['accepted'] += 1

        # Calculate per-problem accuracy
        for problem_id, stats in problem_attempts.items():
            if problem_id not in processed_problems:
                attempts = stats['attempts']
                accepted = stats['accepted']
                accuracy = accepted / attempts if attempts > 0 else 0

                tags = getProblemTags(problem_id)
                processed_problems[problem_id] = tags
                
                # Store accuracy per tag
                for tag in tags:
                    tag_problem_accuracies[tag].append(accuracy)

        value += 50
        if len(submissions) < 50:
            break

    # Calculate average accuracy for each tag
    tag_accuracy = {}
    for tag, accuracies in tag_problem_accuracies.items():
        average_accuracy = (sum(accuracies) / len(accuracies))*100 if accuracies else 0
        tag_accuracy[tag] = average_accuracy

    # Sort tags by accuracy
    strong_tags = sorted(tag_accuracy.items(), key=lambda x: x[1], reverse=True)
    return strong_tags

def account_id(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    user_id = None
    for img_tag in soup.find_all('img'):
        if 'src' in img_tag.attrs:
            src = img_tag.attrs['src']
            if 'avatar' in src:
                user_id = src.split('/')[4].split('?')[0]
                break
    return user_id

# Example usage
url = "https://toph.co/u/arafraihan7"
acId = account_id(url)
strong_tags = analyzeUserSubmissions(acId)
print("Strong Tags and Average Accuracy Rates:")
for tag, accuracy in strong_tags:
    print(f"{tag}: {accuracy:.2f}%")
