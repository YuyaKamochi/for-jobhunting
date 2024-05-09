from typing import Any
from django.views.generic import ListView,FormView
from django.shortcuts import render
from .models import ShopList
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from . import forms
from . import my_functions

# Create your views here.

class MapView(ListView):
    template_name = 'map.html'
    context_object_name = 'ShopList'
    queryset = ShopList.objects.all()

class ExcelView(ListView):
    template_name = 'excel.html'
    context_object_name = 'ShopList'
    queryset = ShopList.objects.all()

class StatisticsView(ListView):
    template_name = 'statistics.html'
    context_object_name = 'ShopList'
    queryset = ShopList.objects.all()

def UpdateDataView(request):
    if request.method == 'POST':
        # POSTデータから値を取得
        row = request.POST.get('row')
        column = request.POST.get('column')
        value = request.POST.get('value')
        if value == 'true': value=True
        if value == 'false': value=False
        id = request.POST.get('id')

        # ここでデータベースの更新などを行う
        try:
            #変更内容が空白の場合エラー（たぶんModelの作り方を変えた方が良い）
            if value==None: raise ValueError("We can't use blank for the database.")

            # id に対応する行を取得
            shop = ShopList.objects.get(id=id)

            # モデルのフィールド名と一致するか確認し、一致する場合のみ値を設定
            if hasattr(shop, column):
                setattr(shop, column, value)
                shop.save()
                
                # クライアントにJSONレスポンスを返す
                response_data = {'message': 'データを更新しました。'}

                # 元のビューにリダイレクト
                return HttpResponseRedirect(reverse('map:excel'))
            else:
                return JsonResponse({'message': '指定された列が存在しません。'}, status=400)
        except ShopList.DoesNotExist:
            return JsonResponse({'message': '指定された ID の行が見つかりません。'}, status=404)
    else:
        # POST以外のHTTPメソッド（GETなど）の場合の処理を記述
        # 通常、POST以外のリクエストはエラーを返すか無視します
        return JsonResponse({'message': '無効なリクエストです。'}, status=400)

class import_list(FormView):
    template_name = 'import_list.html'
    form_class = forms.import_list_form
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context
    
    def form_valid(self, form):
        uploaded_files = self.request.FILES.getlist("visited_file")
        user = self.request.POST.get("user")
        diff_list,notfind_list,user = my_functions.flag_updater(uploaded_files[0],user)
        if uploaded_files[0].name.endswith(".html"):
            context = {'user':user,'diff_list':diff_list,'notfind_list':notfind_list}
            return render(self.request,'form_valid.html',context)
        else:
            context = {'form':form}
            return render(self.request,self.template_name,context)

class AddShopView(FormView):
    template_name= "add_shop.html"
    form_class = forms.ToDatabeseForm
