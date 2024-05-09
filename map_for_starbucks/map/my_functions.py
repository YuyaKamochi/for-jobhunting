def html_reader(file,user):
    from bs4 import BeautifulSoup
    
    html = file.read()
    soup = BeautifulSoup(html, "html.parser")
    elems = soup.find_all(attrs={"class": "modal-trigger"})
    diff = []
    
    for elem in elems:
        store_id = int(elem.attrs["data-store_id"])
        flag = True
        frequency_of_visit = int(elem.attrs["data-frequency_of_visits"])
        last_visit = elem.attrs["data-last_visit"]
        diff.append([store_id,flag,frequency_of_visit,last_visit])
        
    return diff,user

def database_updater(diffs,user):
    from .models import ShopList
    target = ShopList.objects
    id_list = []
    
    for t in target.all():
        id_list.append(getattr(t, "id"))
    
    true_list = []
    notfind_list = []
    check_list = []

    for diff in diffs:
        store_id = diff[0]
        flag = diff[1]
        frequency_of_visit = diff[2]
        last_visit = diff[3]
        check_list.append(store_id)
        if target.filter(id=store_id).exists():
            shop = target.get(id=store_id)
            if getattr(shop,str(user)) != flag:
                true_list.append(getattr(shop, "name"))
            setattr(shop, str(user), flag)
            if str(user) == "yuya":
                setattr(shop, "yuya_frequency_of_visit", int(frequency_of_visit))
                setattr(shop, "yuya_last_visit", last_visit)
            elif str(user) == "non":
                setattr(shop, "non_frequency_of_visit", int(frequency_of_visit))
                setattr(shop, "non_last_visit", last_visit)
            shop.save()
        else:
            notfind_list.append(store_id)
    
    for id in list(set(check_list) - set(id_list) - set(notfind_list)):
        t = target.get(id=int(id))
        setattr(t, str(user), False)
        t.save()
        
    return true_list,notfind_list

def test_func():
    path = r"C:\Users\kunik\Downloads\マイストアパスポート｜スターバックス コーヒー ジャパン.html"
    file = open(path,encoding="utf-8")
    user = 'yuya'
    diff,user = html_reader(file,user)
    database_updater(diff,user)
    
def flag_updater(file,user):
    diff,user = html_reader(file,user)
    diff_list,notfind_list = database_updater(diff,user)
    return diff_list,notfind_list,user

if __name__ == "__main__":
    test_func()