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

    login: ({id, password, success, failure}) ->
        obj = this
        event = $.ajax do
            type: 'POST'
            url: '/login'
            data:
                id: id
                password: password
        event.done ->
            obj.set 'loggedUser' id
            success!
        event.fail ->
            obj.set 'loggedUser' null
            failure!

    logout: ({success, failure}) ->
        obj = this
        event = $.ajax do
            type: 'POST'
            url: '/logout'
        event.done ->
            obj.set 'loggedUser' null
            success!
        event.fail ->
            failure!

App.AuthState = AuthState.create!

App.Router.map ->
    @route "index",
        path: "/"
    @route "register",
        path: '/register'

App.IndexRoute = Ember.Route.extend do
    renderTemplate: ->
        @render 'navbar',
            controller: 'navbar'
            outlet: 'navbar'

App.NavbarController = Ember.Controller.extend do
    loginId: null
    loginPassword: null
    currentlyLoggingIn: false
    login: ->
        ctrl = this
        @.set 'currentlyLoggingIn' true
        App.AuthState.login do
            id: @get 'loginId'
            password: @get 'loginPassword'
            success: -> ctrl.set 'currentlyLoggingIn' false
            failure: -> ctrl.set 'currentlyLoggingIn' false
    logout: ->
        App.AuthState.logout do
            success: ->
            failure: ->

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
        $ @get 'contentElement' .hide!
        @$!click ->
            $ view.get 'contentElement' .show!
            setTimeout (-> this.$ 'input:first' .focus!), 100
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
