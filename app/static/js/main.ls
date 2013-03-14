window.App = Ember.Application.create!

App.Store = DS.Store.extend do
    revision: 12

App.User = DS.Model.extend do
    foo: 'bar'

AuthState = Ember.Object.extend do
    loggedUser: null

    init: ->
        obj = this
        event = $.ajax do
            type: 'GET'
            url: '/logged_user'
        event.done (data) ->
            if 'logged_user' of data
                obj.set 'loggedUser' App.User.find data['logged_user']
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
            obj.set 'loggedUser' App.User.find id
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
        @render 'index',
            outlet: 'main'

App.RegisterRoute = Ember.Route.extend do
    renderTemplate: ->
        @render 'navbar',
            controller: 'navbar'
            outlet: 'navbar'
        @render 'register',
            outlet: 'main'

App.NavbarController = Ember.Controller.extend do
    loginId: null
    loginPassword: null
    loginErrors: Ember.A!
    currentlyLoggingIn: false

    login: ->
        id = @get 'loginId'
        pass = @get 'loginPassword'
        ctrl = this
        @set 'loginErrors' Ember.A!

        if not id
            @set 'loginErrors' Ember.A ['Syötä käyttäjätunnus.']
            return

        if not pass
            @set 'loginErrors' Ember.A ['Syötä salasana.']
            return

        @.set 'currentlyLoggingIn' true
        App.AuthState.login do
            id: id
            password: pass
            success: ->
                ctrl.set 'loginId' null
                ctrl.set 'loginPassword' null
                ctrl.set 'currentlyLoggingIn' false
            failure: ->
                ctrl.set 'loginErrors' Ember.A ['Virheellinen käyttäjätunnus tai salasana.']
                ctrl.set 'currentlyLoggingIn' false
    logout: ->
        App.AuthState.logout do
            success: ->
            failure: ->

App.Popover = Ember.View.extend do
    tagName: 'a'
    template: Ember.Handlebars.compile '{{ view.label }}'
    attributeBindings: ['href']
    href: 'javascript:;'
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
    href: 'javascript:;'
    didInsertElement: ->
        this.$!dropdown!
