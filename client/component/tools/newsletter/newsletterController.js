myapp.controller("newsletterController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location", "$timeout",

    function($scope, $rootScope, $http, $routeParams, $location, $timeout) {
        // create a message 
        console.log('newsletterController');


        $scope.lista_news = [];
        $scope.genereted = false






        $scope.cerca = function(articolo) {
            $http.get('/tools/articolo_superato/find_articolo/' + articolo).then(function(resp) {
                $scope.info_art = resp.data
            });
        }




        $scope.inserisci = function(articolo, codice) {
            articolo.codice = codice
            $scope.lista_news.push(articolo)
        }



        $scope.remove = function(index) {
            $scope.lista_news.splice(index, 1)
        }


        $scope.genera = function() {

            $scope.loading = true;


            $http.post('/tools/newsletter/generate/', $scope.lista_news).then(function(resp) {
                $scope.respo = resp.data

                setTimeout(() => {
                    $location.path('/tools/newsletter/generated')
                    $scope.$apply()
                    window.location.reload();

                    $scope.loading = false;

                    // And any other code that should run only after 5s
                }, 5000);

            });


        }




    }
]);