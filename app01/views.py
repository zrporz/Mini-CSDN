import time

from django.shortcuts import render, HttpResponse

now_page = 0
lan_dict = {'Cpp': None, 'C': None, 'Python': None, "Java": None, "JavaScript": None, "SQL": None, "PHP": None,
            "Others": None}
order = 1
search_content = ""
ONEPAGENUM = 20


def index(request):
    return HttpResponse("欢迎使用")


def user_list(request):
    name = "我爱小学期！"
    roles = ['老师', '学生', '助教']
    user_info = {"name": "华子", "salary": 100000, 'roles': 'teacher'}
    return render(request, "user_list.html", {"n1": name, "n2": roles, 'n3': user_info})


def link_view(request):
    import json
    with open('app01/static/data/link_test.json', 'r', encoding='utf-8') as JsonFile:
        link_data = json.load(JsonFile)
    return render(request, "link_test.html", {"n1": link_data})


def link_blog(request):
    import json
    import markdown
    from django.template.loader import get_template
    import re
    import time
    # try:
    #     dict1 = request.GET
    #     context = dict1.get('context')
    #     name = dict1.get('name')
    # except:
    #     context = None
    #     name = None
    with open('app01/static/data/all_data.json', 'r', encoding='utf-8') as JsonFile:
        try:
            page = int(request.GET.get('id'))
            global now_page
            now_page = page
        except:
            page = now_page
        with open('app01/static/data/all_comments.json', 'r+', encoding='utf-8') as CommentsFile:
            all_comments = json.load(CommentsFile)
            comments_content = all_comments[page]
            post_test = request.GET.get('post_test')
            if post_test is not None:
                # comments_content.append([post_test, time.localtime()])
                comments_content.append([post_test, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())])
            # if len(comments_content) is not 0:
            did = request.GET.get('did')
            if did is not None:
                for x in comments_content:
                    if x[1] == did:
                        comments_content.remove(x)
                        break
            all_comments[page] = comments_content
            comments = [list(reversed(comments_content)), len(comments_content)]
            # else:
            #     comments = [comments_content, len(comments_content)]

            CommentsFile.seek(0)
            CommentsFile.truncate()
            CommentsFile.write(json.dumps(all_comments, ensure_ascii=False))

        all_data = json.load(JsonFile)
        exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
                'markdown.extensions.toc']
        all_data[page]['Content'] = markdown.markdown(all_data[page]['Content'], extensions=exts)
        all_data[page]['Content'] = re.sub(r'src="C:/Users/tehaj/Desktop/PythonHomework/Beta/src/content/(\w+.\w+)" ',
                                           "src=\" /static/img/content/\\g<1> \"", all_data[page]['Content'])
        all_data[page]['AuthorPic'] = re.sub(r'C:/Users/tehaj/Desktop/PythonHomework/Beta/src/portrait/(\w+.\w+)',
                                             " /static/img/portrait/\\g<1> ", all_data[page]['AuthorPic'])
        if all_data[page]['language'].count('Cpp') is not 0:
            all_data[page]['language'][all_data[page]['language'].index('Cpp')] = 'C++'
        if all_data[page]['language'].count('Csharp') is not 0:
            all_data[page]['language'][all_data[page]['language'].index('Csharp')] = 'C#'
    template = get_template('SingleBlog.html')
    result = template.render({'Data': all_data[page], 'Com': comments})

    return HttpResponse(result)
    # return render(request, "SingleBlog.html", {'Data': all_data[0]})


def start(request):
    import json
    import markdown
    from django.template.loader import get_template
    import re
    import random
    with open('app01/static/data/all_data.json', 'r', encoding='utf-8') as JsonFile:
        all_data = json.load(JsonFile)
        # print(len(all_data))
        rec_index = []
        num = 0
        while num < 20:
            _index = random.randint(0, len(all_data))
            if _index in rec_index:
                continue
            else:
                rec_index.append(_index)
                num = num + 1
        with open('app01/static/data/all_comments.json', 'r', encoding='utf-8') as CommentsFile:
            all_comments = json.load(CommentsFile)
            # for i in rec_index:
            #     if  all_comments[i] is None:
            #        all_comments[i] = 0
            #     else:
            #         all_comments[i] = len(all_comments[i])
            rec_list = [[all_data[i], len(all_comments[i]), i] for i in rec_index]

        # context = request.session.get('msg')

    return render(request, 'Start.html', {'Data': rec_list})


def has_same(list1: list, list2: list):
    result = False
    for x in list1:
        for y in list2:
            if x == y:
                result = True
    return result


def search(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    import json
    import re
    import time
    global order, search_content
    T1 = time.time()
    order = request.GET.get('order', order)
    print(type(order), order)
    search_content = request.GET.get('search_content', search_content)
    print(type(search_content), search_content)
    try:

        cpp = request.GET.get('Cpp', None)
        c = request.GET.get('C', None)
        python = request.GET.get('Python', None)
        java = request.GET.get('Java', None)
        javascript = request.GET.get('JavaScript', None)
        sql = request.GET.get('SQL', None)
        php = request.GET.get('PHP', None)
        others = request.GET.get('Others', None)

        lan_dict = {'Cpp': cpp, 'C': c, 'Python': python, "Java": java, "JavaScript": javascript, "SQL": sql,
                    "PHP": php,
                    "Others": others}
        print(lan_dict)
        ans = 0
        for i in lan_dict:
            if lan_dict[i] is "1":
                ans = 1
        if ans == 0:
            for i in lan_dict:
                lan_dict[i] = 1
    except:
        print('nothing')

    lan_list = []
    for x in lan_dict:
        if lan_dict[x] is not None:
            lan_list.append(x)
    print(lan_list)
    rec_list = []
    with open('app01/static/data/all_comments.json', 'r', encoding='utf-8') as CommentsFile:
        all_comments = json.load(CommentsFile)
    T3=time.time()
    with open('app01/static/data/all_data.json', 'r', encoding='utf-8') as JsonFile:
        all_data = json.load(JsonFile)
        for each in all_data:

            if has_same(each['language'], lan_list) is True and (
                    each['Content'].find(search_content) != -1 or each['Title'].find(search_content) != -1):
                _date_ = re.match(r'(\d+)-(\d+)-(\d+)', each['Date']).group(1) + re.match(r'(\d+)-(\d+)-(\d+)',
                                                                                          each['Date']).group(
                    2) + re.match(r'(\d+)-(\d+)-(\d+)', each['Date']).group(3)
                _time_ = re.match(r'(\d+):(\d+):(\d+)', each['Time']).group(1) + re.match(r'(\d+):(\d+):(\d+)',
                                                                                          each['Time']).group(
                    2) + re.match(r'(\d+):(\d+):(\d+)', each['Time']).group(3)
                _index_ = all_data.index(each)
                each.update({'ForTimeCompare': _date_ + _time_})

                rec_list.append([each, len(all_comments[_index_]), _index_])
    T4 = time.time()
    print(T4-T3)
    if order == '1':
        rec_list.sort(key=lambda _: _[0]['ForTimeCompare'], reverse=True)

    else:
        rec_list.sort(key=lambda _: int(_[0]['Likes']), reverse=True)

    paginator = Paginator(rec_list, ONEPAGENUM)
    page = request.GET.get("page", 1)
    try:
        current_page = int(page)
    except:
        current_page = 1

    page_left = current_page - 1
    page_right = current_page + 1
    ell_left = current_page - 2
    ell_right = current_page + 2
    page_end = paginator.num_pages

    try:
        now_page_list = paginator.page(current_page)
        print('Hello')
    except PageNotAnInteger:
        now_page_list = paginator.page(1)
        print('No')
    except EmptyPage:
        now_page_list = paginator.page(paginator.num_pages)
        print('Empty')
    T2 = time.time()
    time_used = int((T2 - T1) * 1000)
    search_num = len(rec_list)
    return render(request, 'Search.html',
                  {'Data': now_page_list, 'lan_dict': lan_dict, 'order': order, 'search_content': search_content,
                   'page_left': page_left, 'page_right': page_right, 'ell_left': ell_left, 'ell_right': ell_right,
                   'page_end': page_end, 'time_used': time_used, 'search_num': search_num})


def category(request):
    import json

    lan_num_dict = {'Cpp': 0, 'Python': 0, 'Csharp': 0, 'Java': 0, 'JavaScript': 0, 'SQL': 0, 'PHP': 0, 'Others': 0}
    with open('app01/static/data/all_data.json', 'r', encoding='utf-8') as JsonFile:
        all_data = json.load(JsonFile)
        for each in all_data:
            for i in lan_num_dict:
                if i in each['language']:
                    lan_num_dict[i] = lan_num_dict[i] + 1

    all_num = len(all_data)
    return render(request, 'Category.html', {'Data': lan_num_dict, 'AllNum': all_num})


def show(request):
    import json
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    with open('app01/static/data/all_data.json', 'r', encoding='utf-8') as JsonFile:
        all_data = json.load(JsonFile)
    with open('app01/static/data/all_comments.json', 'r', encoding='utf-8') as CommentsFile:
        all_comments = json.load(CommentsFile)
    cat = request.GET.get('category')
    rec_list = []
    if cat == 'All':
        for each in all_data:
            _index_ = all_data.index(each)
            rec_list.append([each, len(all_comments[_index_]), _index_])
    else:
        for each in all_data:
            if cat in each['language']:
                _index_ = all_data.index(each)
                rec_list.append([each, len(all_comments[_index_]), _index_])

    paginator = Paginator(rec_list, ONEPAGENUM)
    page = request.GET.get("page", 1)
    try:
        current_page = int(page)
    except:
        current_page = 1
    if current_page not in range(1, paginator.num_pages + 1):
        print("Invalid input!")
        current_page = 1
    page_left = current_page - 1
    page_right = current_page + 1
    ell_left = current_page - 2
    ell_right = current_page + 2
    page_end = paginator.num_pages

    try:
        now_page_list = paginator.page(current_page)
        print('Hello')
    except PageNotAnInteger:
        now_page_list = paginator.page(1)
        print('No')
    except EmptyPage:
        now_page_list = paginator.page(paginator.num_pages)
        print('Empty')
    pic_path = "img/background/" + cat + ".jfif"

    return render(request, 'Show.html',
                  {'Data': now_page_list, 'category': cat,
                   'page_left': page_left, 'page_right': page_right, 'ell_left': ell_left, 'ell_right': ell_right,
                   'page_end': page_end, 'pic_path': pic_path})
