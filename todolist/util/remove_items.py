from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


def remove_item_view(model, redirect_url_pattern_name):
    """
    Returns a function (that works as a view) that will remove an object from the table that is being controlled by a
    certain model.  The url pattern that this view should be bound to should look something like: "<...>/<int:id>".
    In this case, <id> pertains to the ID of the object in the table specified.
    :param model: The model that controls the table we want to manipulate.  (i.e. if we want to remove problems, pass
    in the Problem class to remove those)
    :param redirect_url_pattern_name: This view will return a redirect to another URL.  The URL will be determined by
    the url pattern name specified for this argument
    :return: A function as specified above
    """

    @login_required(login_url='login/')
    def func(req, id):
        obj = get_object_or_404(model, pk=id)
        if obj.user == req.user:
            obj.delete()
            messages.success(req, 'Success!')
        else:
            messages.error(req, 'Insufficient permissions! (you are not the owner of this entry)')

        return redirect(redirect_url_pattern_name)

    return func
