var myapp = angular.module('myapp', ['ngRoute', 'ngResource', 'ngSanitize']);
myapp.config(function($httpProvider) {
    //Enable cross domain calls
    $httpProvider.defaults.useXDomain = true;

    //Remove the header used to identify ajax call  that would prevent CORS from working
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
});

// configure our routes
myapp.config(function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: './component/home.html'
        })
        .when('/agenti', {
            templateUrl: './component/dashboard/agenti/dashboard.html',
            controller: 'dashboard_agentiController'
        })
        .when('/admin', {
            templateUrl: './component/dashboard/admin/dashboard.html',
            controller: 'dashboard_adminController'
        })
        .when('/info_articolo', {
            templateUrl: './component/dashboard/info_articolo/info_articolo.html',
            controller: 'info_articoloController'
        })
        .when('/statistiche_clienti', {
            templateUrl: './component/dashboard/statistiche_clienti/statistiche_clienti.html',
            controller: 'statistiche_clientiController'
        })
        .when('/listini_promozionali', {
            templateUrl: './component/dashboard/listini_promozionali/listini_promozionali.html',
            controller: 'listini_promozionaliController'
        })


    .when('/tools/articoli_superati', {
            templateUrl: './component/tools/articoli_superati/articoli_superati.html',
            controller: 'articoli_superatiController'
        })
        .when('/tools/aumento_prezzi_di_acquisto', {
            templateUrl: './component/tools/variazione_prezzi/aumento_prezzi_di_acquisto.html',
            controller: 'aumento_prezzi_di_acquistoController'
        })
        .when('/tools/newsletter', {
            templateUrl: './component/tools/newsletter/insert_newsletter.html',
            controller: 'newsletterController'
        })
        .when('/tools/newsletter/generated', {
            templateUrl: './component/tools/newsletter/report.html',
            controller: 'newsletterController'
        })
        /*     .when('/tools/offerte', {
                templateUrl: './component/tools/offerte/offerte.html',
                controller: 'template_offerteController'
            }) */
        .when('/tools/stato_magazzino/lista_stato_oridni', {
            templateUrl: './component/tools/stato_magazzino/lista_stato_ordini.html',
            controller: 'stato_ordini_magazzinoController'
        })
        .when('/tools/stato_magazzino/QRCode_generate', {
            templateUrl: './component/tools/stato_magazzino/QRCode_generate.html',
            controller: 'new_qrcode_magazzino'
        })
        .when('/tools/generatore_kit/generatore_kit', {
            templateUrl: './component/tools/generatore_kit/generatore_kit.html',
            controller: 'generatore_kitController'
        })



    .when('/rs/articoli', {
            templateUrl: './component/ricerca_sviluppo/omnia/articoli/articoli.html',
            controller: 'articoliController'
        })
        .when('/rs/last_letture', {
            templateUrl: './component/ricerca_sviluppo/omnia/last_letture/last_letture.html',
            controller: 'last_lettureController'
        })
        .when('/rs/letture', {
            templateUrl: './component/ricerca_sviluppo/omnia/letture/letture.html',
            controller: 'lettureController'
        })
        .when('/rs/storico_variazioni', {
            templateUrl: './component/ricerca_sviluppo/omnia/storico_variazioni/storico_variazioni.html',
            controller: 'storico_variazioniController'
        })



    .when('/rs/campioni', {
        templateUrl: './component/ricerca_sviluppo/campioni/campioni.html',
        controller: 'campioniController'
    })

    .when('/rs/campioni/:tipo', {
        templateUrl: './component/ricerca_sviluppo/campioni/tipo.html',
        controller: 'tipo_Controller'
    })

    .when('/rs/campioni/:tipo/:stato', {
            templateUrl: './component/ricerca_sviluppo/campioni/stato_campioni.html',
            controller: 'stato_campioniController'
        })
        .when('/rs/campione/:id', {
            templateUrl: './component/ricerca_sviluppo/campioni/widget/articolo.html',
            controller: 'articolo_Controller'
        })

    .when('/rs/new_campioni', {
            templateUrl: './component/ricerca_sviluppo/campioni/new_campioni.html',
            controller: 'new_campioniController'
        })
        .when('/rs/campioniall/campioni_tot/', {
            templateUrl: './component/ricerca_sviluppo/campioni/campioni_tot.html',
            controller: 'campioni_totController'
        })

    .when('/rs/campione/modifica/:id', {
        templateUrl: './component/ricerca_sviluppo/campioni/new_campioni.html',
        controller: 'new_campioniController'
    })


    .when('/officina/lavorazione', {
            templateUrl: './component/officina/lavorazione.html',
            controller: 'lavorazioneController'
        })
        .when('/officina/lavorazione/:id', {
            templateUrl: './component/officina/tipo_lavorazione.html',
            controller: 'tipo_lavorazioneController'
        })
        .when('/officina/lavorazione/:id/:id', {
            templateUrl: './component/officina/dettaglio_lavorazione.html',
            controller: 'dettaglio_lavorazioneController'
        })



    .when('/utenti/gestione_utenti', {
        templateUrl: './component/utenti/gestione_utenti.html',
        controller: 'gestione_utentiController'
    })

});