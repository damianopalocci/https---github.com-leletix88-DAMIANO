myapp.controller("mainController", [
    "$scope", "$http", "$routeParams", "$location", "$rootScope", "$timeout",

    function($scope, $http, $routeParams, $location, $rootScope, $timeout) {
        // create a message 
        console.log('mainController');

        $rootScope.current_page = $location.path()


        $http
            .get("/login_service")
            .then(function(response) {
                $timeout(function() {

                    $rootScope.login_info = response.data;


                    if (response.data.username == 'apolidori') { $location.path('/tools/stato_magazzino/QRCode_generate') }



                });


            });





    }
]);