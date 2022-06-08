myapp.controller("articoli_superatiController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('articoli_superatiController');





        $scope.cerca = function(articolo) {


            $http.get('/tools/articolo_superato/find_articolo/' + articolo).then(function(resp) {


                $scope.info_art = resp.data


            });

        }



    }
]);