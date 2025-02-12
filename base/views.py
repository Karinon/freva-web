import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
from django_evaluation.monitor import _restart
from django.conf import settings
from django.urls import reverse
from evaluation_system.misc import config
from django.utils.http import url_has_allowed_host_and_scheme


@sensitive_variables("passwd")
@sensitive_post_parameters("password")
def home(request):
    """Default view for the root"""
    login_failed = False
    guest_login = None

    next_page = request.GET.get("next", None)
    forward = request.POST.get("next", None)
    if not request.user.is_authenticated:
        try:
            username = request.POST.get("user", "")
            passwd = request.POST.get("password", "")
            if username:
                user_object = auth.authenticate(username=username, password=passwd)
                if user_object:
                    auth.login(request, user_object)
                    guest_login = user_object.isGuest()
                    if forward and url_has_allowed_host_and_scheme(
                        forward, allowed_hosts=request.get_host()
                    ):
                        return HttpResponseRedirect(forward)
                    else:
                        return HttpResponseRedirect("/")

                else:
                    raise Exception("Login failed")

        except Exception as e:
            # do not forget the forward after failed login
            if forward:
                next_page = forward

            login_failed = True
            logging.error(str(e))

    return render(
        request,
        "base/home.html",
        {"login_failed": login_failed, "guest_login": guest_login, "next": next_page},
    )


def dynamic_css(request):
    main_color = settings.MAIN_COLOR
    hover_color = settings.HOVER_COLOR
    border_color = settings.BORDER_COLOR
    return render(
        request,
        "base/freva.css",
        {
            "main_color": main_color,
            "hover_color": hover_color,
            "border_color": border_color,
        },
        content_type="text/css",
    )


def wiki(request):
    """
    View rendering the iFrame for the wiki page.
    """
    return render(
        request,
        "base/wiki.html",
        {
            "page": "https://freva.gitlab-pages.dkrz.de/evaluation_system/sphinx_docs/index.html"
        },
    )


@login_required()
def shell_in_a_box(request):
    """
    View for the shell in a box iframe
    """
    if request.user.groups.filter(
        name=config.get("external_group", "noexternalgroupset")
    ).exists():
        shell_url = "/shell2/"
    else:
        shell_url = "/shell/"

    return render(request, "base/shell-in-a-box.html", {"shell_url": shell_url})


@login_required()
def contact(request):
    """
    View rendering the iFrame for the wiki page.
    """
    if request.method == "POST":
        from templated_email import send_templated_mail
        from django_evaluation.ldaptools import get_ldap_object

        user_info = get_ldap_object()
        myinfo = user_info.get_user_info(str(request.user))
        try:
            myemail = myinfo[3]
            username = request.user.get_full_name()
        # TODO: Exception too broad!
        except:
            myemail = settings.SERVER_EMAIL
            username = "guest"
        mail_text = request.POST.get("text")
        send_templated_mail(
            template_name="mail_to_admins",
            from_email=myemail,
            recipient_list=settings.CONTACTS,
            context={
                "username": username,
                "text": mail_text,
                "project": config.get("project_name"),
                "website": config.get("project_website"),
            },
            headers={"Reply-To": myemail},
        )
        return HttpResponseRedirect("%s?success=1" % reverse("base:contact"))
    success = True if request.GET.get("success", None) else False
    return render(request, "base/contact.html", {"success": success})


def logout(request):
    """
    Logout view.
    """
    auth.logout(request)
    return HttpResponseRedirect("/")


@login_required()
@user_passes_test(lambda u: u.is_superuser)
def restart(request):
    """
    Restart form for the webserver
    """
    try:
        if request.POST["restart"] == "1":
            _restart(path=None)
    # TODO: Exception too broad!
    except:
        return render(request, "base/restart.html")

    return render(request, "base/home.html")
