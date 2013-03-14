window.App = Ember.Application.create!

AuthState = Ember.Object.extend do
    loggedUser: null

    init: ->
        obj = this
        event = $.ajax do
            type: 'GET'
            url: '/logged_user'
        event.done (data) ->
            if 'logged_user' of data
                obj.set 'loggedUser' data['logged_user']
            else
                obj.set 'loggedUser' null

    login: (id, password) ->
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
    loginId: null
    loginPassword: null
    login: ->
        App.AuthState.login @get('loginId'), @get('loginPassword')
    logout: ->
        App.AuthState.logout!

App.Popover = Ember.View.extend do
    tagName: 'a'
    template: Ember.Handlebars.compile '{{ view.label }}'
    attributeBindings: ['href']
    href: '#'
    label: 'Popover'
    placement: 'bottom'
    contentElement: ''
    didInsertElement: ->
        view = this
        $ @get 'contentElement' .hide()
        @$!click ->
            $ view.get 'contentElement' .show()
        this.$!popover do
            content: $ @get 'contentElement'
            placement: @get 'placement'
            html: true

App.Dropdown = Ember.View.extend do
    tagName: 'a'
    classNames: ['dropdown-toggle']
    attributeBindings: ['href', 'id']
    id: ''
    href: '#'
    didInsertElement: ->
        this.$!dropdown!
