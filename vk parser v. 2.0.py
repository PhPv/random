import requests
import json
import time

our_group_id = '-182051949'
access_token = '80dc063b9e0a8529c4397ae8ff982a9522420bfc57010e70ff4afc3c225c0993c45b377e0061298c6240b'
v = 5.95
n = 0
j = 0

# from_group_id = '-174073334'
# all_from_group_id = ['-174073334','-66237897']
all_from_group_id = ['-153111814', '-58150354']
all_posts_our = []
all_posts_their = []
all_rep_id_our = []
all_rep_id_their = []


def wall_get(group_id):
    all_posts = []
    r_our = requests.get('https://api.vk.com/method/wall.get?' + 'owner_id=' + group_id + '&v=' + str(
        v) + '&access_token=' + access_token)
    post = r_our.json()['response']['items'][0]
    all_posts.extend(r_our.json()['response']['items'])
    write_json(all_posts)
    print(all_posts)
    return all_posts


# записывает в файл с именем posts.json переменную указанную в скобках к вызову функции
# (вместо data) для коренной группы
def write_json(data):
    global j
    with open(str(j) + 'posts.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        j += 1


# записывает в файл с именем posts.json переменную указанную в скобках к вызову функции (вместо data)
# для репостящихся групп
def write_their_json(data):
    with open('all_group.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


# функция выборки инофрмации. Пробуется выбор айди поста, айди репоста, айди репостящей группы.
# Есди неудачно, то значит группа чужая и надо идти по второму алгоритму.
# Формат выдачи данных различается. У репостов больше уровней.
# Сейчас работает не правильно для родной группы. Алгоритм должен для своей группы пропускать блок трай


def get_info_from_our(post):
    try:
        our_post_id = post['id']
        their_post_id = post['copy_history'][0]['id']
        their_post_from_id = post['copy_history'][0]['from_id']
        rep_id = str(their_post_from_id) + "_" + str(their_post_id)
    except:
        pass
    data_our = {
        'post_id': our_post_id,
        'rep_id': rep_id
    }
    return data_our


def get_info_from_their(allpost):
    try:
        their_post_id = allpost['id']
        their_post_from_id = allpost['from_id']
        rep_id = str(their_post_from_id) + "_" + str(their_post_id)
    except:
        their_post_id = 0
        rep_id = 0
    data_their = {
        'post_id': their_post_id,
        'rep_id': rep_id
    }
    return data_their


# Главная функция.
# использует метод волл гет чтобы взять информацию со стены, выбираются нужные элементы,
# формируется список оллпостс и сохраняется список в джейсон файл для корневой группы

def get_rep_id_from_our(our_post):
    our_posts = get_info_from_our(our_post)
    rep_id_our = our_posts.get("rep_id")
    all_rep_id_our.append(rep_id_our)
    return all_rep_id_our


all_posts_our = wall_get(our_group_id)
for post in all_posts_our:
    all_rep_id_our = get_rep_id_from_our(post)


def get_rep_id_from_their(their_post):
    their_posts = get_info_from_their(their_post)  # ошибка
    rep_id_their = their_posts.get("rep_id")
    all_rep_id_their.append(rep_id_their)
    return all_rep_id_their


# завернуть блок сравнения в функцию


def main():
    for from_group_id in all_from_group_id:
        all_posts_their = wall_get(from_group_id)
        for post in all_posts_their:
            all_rep_id_their = get_rep_id_from_their(post)
        for rep_id_their in all_rep_id_their:
            for rep_id_our in all_rep_id_our:
                if rep_id_our == rep_id_their:
                    x = 1
                    break
                else:
                    x = 0
            if x == 0 and n < 1:
                print("Репостим" + str(rep_id_their))
                repost(rep_id_their)


def repost(rep_id):
    # repost = requests.get('https://api.vk.com/method/wall.repost?' + 'object=wall' + rep_id + '&' + 'group_id=' + our_group_id.replace('-', '') +'&v=' + str(v) + '&access_token=' + access_token)
    print("зарепостили" + str(rep_id))
    global n
    n += 1
    time.sleep(1)


if __name__ == '__main__':
    main()

while True:
    main()
    time.sleep(60)
    break
