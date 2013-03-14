window.App = Ember.Application.create!

AuthState = Ember.Object.extend do
    loggedUser: null
    login: !(id, password) ->
        obj = this
        event = $.ajax do
            type: 'POST'
            url: '/login'
            data:
                id: id
                password: password
        event.done ->
            obj.set 'loggedUser' id
        event.fail ->
            obj.set 'loggedUser' null
    logout: ->
        obj = this
        event = $.ajax do
            type: 'POST'
            url: '/logout'
        event.done ->
            obj.set 'loggedUser' null

App.AuthState = AuthState.create!

App.Router.map ->
    @route "index",
        path: "/"

App.IndexRoute = Ember.Route.extend do
    renderTemplate: ->
        @render 'navbar',
            controller: 'navbar'
            outlet: 'navbar'

App.NavbarController = Ember.Controller.extend do
    foo: 'bar'
