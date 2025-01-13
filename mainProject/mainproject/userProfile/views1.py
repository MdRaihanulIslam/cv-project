from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .forms import updateInfoForm
import requests
from bs4 import BeautifulSoup
from collections import defaultdict


# Create your views here.
def Profile(request):
    return render(request,'userProfile/html/profile.html')

def get_codeforces_submissions(handle):
    url = 'https://codeforces.com/api/user.status?handle='+handle
    try:
        response = requests.get(url)
        data = response.json()
        Size = 0
        if data['status']=='OK':
            submissions = data['result']
            Size = len(submissions)
        return Size
    except:
        return HttpResponse("Unexpected error!")
    
    import requests

import requests
from collections import defaultdict

def fetch_codeforces_submissions(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return []
    
    data = response.json()
    if data['status'] != 'OK':
        print("Failed to fetch user data.")
        return []
    
    return data['result']

def calculateStrongPointForCf(handle):
    # Fetch all submissions for the user
    submissions = fetch_codeforces_submissions(handle)
    
    if not submissions:
        print("No submissions found.")
        return {}, {}

    # Track stats for each problem and each tag
    problem_stats = defaultdict(lambda: {"attempted": 0, "accepted": 0, "tags": []})
    tag_problem_success_rates = defaultdict(list)  # Stores success rates for each tag

    solved_problems = set()  # To track which problems have been solved

    for submission in submissions:
        # Construct a unique problem identifier
        problem = submission.get('problem', {})
        contest_id = problem.get('contestId')
        index = problem.get('index')
        tags = problem.get('tags', [])
        
        if not contest_id or not index:
            continue
        
        problem_id = f"{contest_id}{index}"
        verdict = submission.get('verdict')

        # If problem is already accepted, ignore further submissions
        if verdict == 'OK' and problem_id not in solved_problems:
            solved_problems.add(problem_id)

        # Count each attempt for the problem
        problem_stats[problem_id]["attempted"] += 1
        
        # Count accepted submissions for the problem
        if verdict == 'OK':
            problem_stats[problem_id]["accepted"] += 1
        
        # Store tags if they are not already saved for this problem
        if not problem_stats[problem_id]["tags"]:
            problem_stats[problem_id]["tags"] = tags

    # Calculate success rate for each problem and associate with each tag
    for problem_id, stats in problem_stats.items():
        if stats["attempted"] > 0:
            problem_success_rate = (stats["accepted"] / stats["attempted"]) * 100
            
            for tag in stats["tags"]:
                tag_problem_success_rates[tag].append(problem_success_rate)

    # Calculate aggregated success rate for each tag based on per-problem success rates
    tag_aggregated_success_rates = {}
    for tag, success_rates in tag_problem_success_rates.items():
        if success_rates:
            aggregated_success_rate = sum(success_rates) / len(success_rates)
            tag_aggregated_success_rates[tag] = aggregated_success_rate

    # Print success rates for each tag based on individual problem rates
    print(f"Success rates for each tag based on individual problems for user {handle}:")
    for tag, rate in tag_aggregated_success_rates.items():
        print(f"- Tag {tag}: {rate:.2f}% success rate")

    return tag_aggregated_success_rates

def updateInfo(request):
    if request.method=='POST':
        Handle_cf = request.POST.get('CodeForces_Handle')
        url_cf = 'https://codeforces.com/api/user.status?handle='+Handle_cf+'&from=1&count=100'
        cf_success = False
        toph_success = False
        try:
            response_cf = requests.get(url_cf)
            if response_cf.status_code==200:
                cf_success = True
            else:
                return JsonResponse({"You have given invalid username!"})
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)
        
        
        Handle_toph = request.POST.get('Toph_Handle')
        url_toph = "https://toph.co/u/"+Handle_toph
        try:
            response_toph = requests.get(url_toph)
            if response_toph.status_code==200:
                toph_success = True
            else:
                return JsonResponse({"You have given invalid username!"})
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)
        
        strong_tags = calculateStrongPointForCf("_Raihan__")
        for strngtag in strong_tags:
            print(strngtag)
        if cf_success and toph_success:
            return HttpResponse("Successfully updated Codeforces and Toph!")
        elif cf_success:
            return HttpResponse("Successfully updated Codeforces!")
        elif toph_success:
            return HttpResponse("Successfully updated Toph!")
        else:
            return JsonResponse({"error": "Failed to update both Codeforces and Toph!"})
        
    else:
        form = updateInfoForm()
        context = {
            'form' : form
        }
        return render(request,'userProfile/html/updateInfo.html',context = context)
    