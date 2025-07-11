import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt


@login_required
def get_all_list_in_category(request, category_id):
    user = request.user
    try:
        content_type = ContentType.objects.get(id=category_id)
        items = List.objects.filter(user=user, content_type=content_type)

        response_data = []
        for item in items:
            related_object = item.content_object
            response_data.append({
                'id' : item.id,
                'title' : related_object.title if related_object else "Без названия",
                'own_rating' : item.rating if item.rating else "Оценки пока нет",
                'rating' : related_object.rating if related_object else "Рейтинга пока нет",
                'note': item.note,
                'img': related_object.img if related_object else "",
            })
        return JsonResponse({'items': response_data})
    except ContentType.DoesNotExist:
        return JsonResponse({'error': 'Категория не найдена'}, status=404)



def get_all_category(request):
    content_types = ContentType.objects.filter(model__in=['anime', 'manga', 'book', 'movie'])
    content_data = []

    def translate(name):
        translations = {"manga": 'МАНГА', 'anime': 'АНИМЕ', 'movie': 'ФИЛЬМЫ', 'book': 'КНИГИ'}
        return translations.get(name)

    for content in content_types:
        content_data.append({
            'id': content.id,
            'model': content.model,
            'name': translate(content.name),
        })

    return JsonResponse({'content_types': content_data})


def index(request):
    return render(request, 'MainPage/index.html')


def add_original_title_in_category(request):
    category = request.GET.get('category')
    if request.method == 'POST':
        user = request.user
        if not User.objects.filter(pk=user.id).exists():
            return JsonResponse({'message': 'No find such user'}, status=401)

        try:
            data = json.loads(request.body)
            title = data.get('title')

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=402)

        if category == "anime":
            Anime.objects.create(
                title=title
            )

        elif category == "movie":
            Movie.objects.create(
                title=title
            )

        elif category == 'book':
            Book.objects.create(
                title=title
            )

        elif category == 'manga':
            Manga.objects.create(
                title=title
            )

        return JsonResponse({'message': 'Good job'}, status=201)

    else:

        return JsonResponse({'message': 'This method false'}, status=404)


def search_title_in_category(request):
    input_name = request.GET.get('input_name')
    category = request.GET.get('category', '').lower()
    print(category)
    model_mapping = {
        "аниме": Anime,
        "фильмы": Movie,
        "манга": Manga,
        "книги": Book,
    }

    if category not in model_mapping:
        return JsonResponse({'error': 'Invalid category'}, status=400)

    model = model_mapping[category]
    titles = model.objects.filter(title__istartswith=input_name.capitalize()).values()

    return JsonResponse({'titles': list(titles)})


def show_all_title_in_category(request):
    category = request.GET.get('category')
    titles = []
    if category == "anime":
        titles = Anime.objects.values()
    elif category == "movie":
        titles = Movie.objects.values()
    elif category == "manga":
        titles = Manga.objects.values()
    elif category == "book":
        titles = Book.objectss.values()
    return JsonResponse({'titles': list(titles)})


def delete_title_from_list(request):
    user = request.user
    title_id = request.GET.get('title_id')
    title = get_object_or_404(List, id=title_id, user=user)
    title.delete()
    return JsonResponse({'success': True})


def sort(request, category_id):
    user = request.user
    sort_by = request.GET.get('sort_by', 'own_rating')
    content_type = ContentType.objects.get(id=category_id)
    items = List.objects.filter(user=user, content_type=content_type)
    if sort_by == 'own_rating':
        items = items.order_by('own_rating').values()
        return JsonResponse({'list': list(items)})
    if sort_by == 'rating':
        items = items.order_by('rating').values()
        return JsonResponse({'list': list(items)})


def edit_title(request, title_id):
    user = request.user
    title = get_object_or_404(List, id=title_id, user=user)
    if request.method == 'GET':
        return JsonResponse({
            'id': title.id,
            'title': title.content_object.title,
            'note': title.note,
            'rating': title.rating,
        })
    elif request.method in ['POST', 'PUT']:
        try:
            data = json.loads(request.body)
            title.note = data.get('note', title.note)
            title.rating = data.get('rating', title.rating)
            title.save()
            return JsonResponse({'message': 'Task updated successfully'})
        except Exception as e:
            return JsonResponse({'message': f'Error updating task: {str(e)}'}, status=400)

    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


def save_title(request):
    if request.method == 'POST':
        user = request.user
        if not User.objects.filter(pk=user.id).exists():
            return JsonResponse({'message': 'No find such user'}, status=401)
        try:
            data = json.loads(request.body)
            title = data.get('title')
            note = data.get('note')
            content_type = data.get('content_type')
            rating = data.get('rating')

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=402)

        if not content_type or not title:
            return JsonResponse({'message': 'Content type and title are required.'}, status=400)

        content_models = {
            'аниме': Anime,
            'фильмы': Movie,
            'манга': Manga,
            'книги': Book,
        }

        model = content_models.get(content_type.lower())
        if not model:
            return JsonResponse({'message': f"Unsupported content type: {content_type}"}, status=400)

        try:
            content_object, created = model.objects.get_or_create(
                title=title,
            )
        except Exception as e:
            return JsonResponse({'message': f"Error creating or retrieving content: {str(e)}"}, status=500)

        try:
            list_item, _ = List.objects.get_or_create(
                user=user,
                content_type=ContentType.objects.get_for_model(model),
                object_id=content_object.id,
                defaults={
                    'rating': rating,
                    'note': note,
                },
            )
        except Exception as e:
            return JsonResponse({'message': f"Error saving to list: {str(e)}"}, status=500)

        return JsonResponse({
            'message': 'Title added successfully.',
            'list_id': list_item.id,
        }, status=201)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)