from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()


rules, page_lists = input.split("\n\n")

rules = rules.split("\n")
page_lists = page_lists.split("\n")

pages_must_precede = {}
for r in rules:
    a, b = r.split('|')
    a = int(a)
    b = int(b)
    pages_must_precede.setdefault(b, set()).add(a)

def evaluate_page_list(page_list, pages_must_precede):
    seen_pages = set()
    all_pages = set(page_list)
    for page in page_list:
        if page not in pages_must_precede:
            seen_pages.add(page)
            continue
        for must_precede in pages_must_precede[page]:
            if must_precede not in all_pages:
                continue
            if must_precede not in seen_pages:
                #print(f"Page {page} should be preceded by page {must_precede}")
                return False
        seen_pages.add(page)
    return True

sol1 = 0
for curr_page_list in page_lists:
    curr_page_list = [int(n) for n in curr_page_list.split(',')]
    #print(curr_page_list, evaluate_page_list(curr_page_list, pages_must_precede))
    if evaluate_page_list(curr_page_list, pages_must_precede):
        sol1 += curr_page_list[len(curr_page_list)//2]

print(f"Part 1: {sol1}")

def reorder_page_list(page_list, pages_must_precede):
    unadded = set(page_list)
    reordered = []
    while len(unadded) > 0:
        relevant_pages_must_precede = {page: [prec for prec in precedes if prec in unadded] for page, precedes in pages_must_precede.items() if page in unadded}
        for page in unadded:
            if page not in relevant_pages_must_precede:
                relevant_pages_must_precede[page] = []
        next_page = min(relevant_pages_must_precede.keys(), key=lambda x: len(relevant_pages_must_precede[x]))
        assert len(relevant_pages_must_precede[next_page]) == 0
        reordered.append(next_page)
        unadded.remove(next_page)
    return reordered

sol2 = 0
for curr_page_list in page_lists:
    curr_page_list = [int(n) for n in curr_page_list.split(',')]
    if not evaluate_page_list(curr_page_list, pages_must_precede):
        curr_page_list = reorder_page_list(curr_page_list, pages_must_precede)
        sol2 += curr_page_list[len(curr_page_list)//2]

print(f"Part 2: {sol2}")
