from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from datetime import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import yaml


from system.common import query as query_helper
from hrm import models as hrm_models
from system.common import routes as navbar
from hrm.forms import trainings as training_form
from helper import decorators as decorator_helper

"""
Template
"""
credential = yaml.load(open('credentials.yaml'), Loader=yaml.FullLoader)
template_version = ''
try:
    template_version = credential['template_version']
    template_version = "hrm/"+template_version
except Exception as e:
    template_version = 'hrm/v1'


@login_required
def list_trainings(request):
    if not request.user.has_perm('hrm.view_training') and not query_helper.has_all_access(request.user):
        messages.warning(request, "Sorry. You don't have permission.")
        return HttpResponseRedirect(reverse('home'))

    current_branch = query_helper.current_user_branch(request)
    routes = navbar.get_formatted_routes(
        navbar.get_routes(request.user), active_page='training')

    if query_helper.has_all_access(request.user):
        trainings = hrm_models.Training.objects.filter(
            branch=current_branch).order_by('start_date')
    else:
        trainings = hrm_models.Training.objects.filter(
            branch=current_branch, branch_accepted=current_branch)

    training = []
    for data in trainings:
        accepted = False
        if current_branch in data.branch_accepted.all():
            accepted = True
        training.append({
            "id": data.id,
            "name": data.name,
            "certification": data.certification,
            "accepted": accepted,
            "date": data.start_date
        })
    if query_helper.has_all_access(request.user):
        trainings = hrm_models.Training.objects.all().order_by("start_date")

    context = {}
    context.update({"trainings": training})
    context.update({"routes": routes})
    context.update({"title": "All Trainings"})

    return render(request, template_version+"/TrainingView/trainings.html", context=context)


@login_required
def delete_training(request, id):
    if not request.user.has_perm('hrm.delete_training') and not query_helper.has_all_access(request.user):
        messages.warning(request, "Sorry. You don't have permission.")
        return HttpResponseRedirect(reverse('home'))

    try:
        training = hrm_models.Training.objects.get(id=id)
        training.delete()
        messages.success(request, "{} successfully deleted.".format(training.name))
        return HttpResponseRedirect(reverse('hrm-trainings'))
    except (Exception, hrm_models.Training.DoesNotExist) as e:
        messages.error(request, "Sorry. Data not found.")
        return HttpResponseRedirect(reverse('home'))

class Trainings(LoginRequiredMixin, View):
    def common(self, request):
        context = {}
        routes = navbar.get_formatted_routes(
            navbar.get_routes(request.user), active_page='training')
        context.update({"routes": routes})
        context.update({"title": "Add Trainings"})
        context.update({"current_user_branch": query_helper.current_user_branch(request)})
        return context

    def get(self, request):
        if not request.user.has_perm('hrm.add_training') and not query_helper.has_all_access(request.user):
            messages.warning(request, "Sorry. You don't have permission.")
            return HttpResponseRedirect(reverse('home'))
        
        context = self.common(request)
        form = training_form.TrainingForm(context['current_user_branch'])
        context.update({"form": form})
        return render(request, template_version+"/TrainingView/add.html", context=context)


    def post(self, request):
        if not request.user.has_perm('hrm.add_training') and not query_helper.has_all_access(request.user):
            messages.warning(request, "Sorry. You don't have permission.")
            return HttpResponseRedirect(reverse('home'))

        context = self.common(request)
        form = training_form.TrainingForm(context['current_user_branch'], request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            form.save_m2m()
            messages.success(request, "New training successfully added.")
            return HttpResponseRedirect(reverse('hrm-trainings'))
        else:
            context.update({"form": form})

        return render(request, template_version+"/TrainingView/add.html", context=context)


class TrainingsEdit(LoginRequiredMixin, View):
    def common(self, request, name):
        context = {}
        routes = navbar.get_formatted_routes(
            navbar.get_routes(request.user), active_page='training')
        context.update({"routes": routes})
        context.update({"current_user_branch": query_helper.current_user_branch(request)})
        context.update({"title": name})
        return context

    def has_training(self, id):
        try:
            training = hrm_models.Training.objects.get(id=id)
            return True, training
        except Exception as e:
            return False, '' 

    def get(self, request, id):
        if not request.user.has_perm('hrm.view_training') and not query_helper.has_all_access(request.user):
            messages.warning(request, "Sorry. You don't have permission.")
            return HttpResponseRedirect(reverse('home'))

        training = self.has_training(id)

        if not training[0]:
            messages.error(request, "Data not found.")
            return HttpResponseRedirect(reverse('hrm-trainings'))

        training[1].views = training[1].views + 1
        training[1].save()
        context = self.common(request, training[1].name)


        form = training_form.TrainingForm(current_branch = context['current_user_branch'], instance=training[1])
        context.update({"form": form})
        return render(request, template_version+"/TrainingView/edit.html", context= context)

    def post(self, request, id):
        if not request.user.has_perm('hrm.change_training') and not query_helper.has_all_access(request.user):
            messages.warning(request, "Sorry. You don't have permission.")
            return HttpResponseRedirect(reverse('home'))

        training = self.has_training(id)
        if not training[0]:
            messages.warning(request, "Sorry. Data not found.")
            return HttpResponseRedirect(reverse('hrm-trainings'))

        context = self.common(request, training[1].name)
        form = training_form.TrainingForm(context['current_user_branch'], request.POST, instance=training[1])

        if form.is_valid():
            new_data = form.save(commit=False)
            new_data.save()
            form.save_m2m()
            messages.success(request, "Data successfully updated.")
            return redirect(request.META['HTTP_REFERER'])
        else:
            context.update({"form": form})
            return render(request, template_version+"/TrainingView/edit.html", context=context)
