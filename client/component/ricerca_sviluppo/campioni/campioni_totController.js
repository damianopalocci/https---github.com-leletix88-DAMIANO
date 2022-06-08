myapp.controller("campioni_totController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('campioni_totController');


        $http.get('/tools/campioni/getcampioni').then(function(resp) {
            $scope.db_campioni_tot = resp.data
        });



        $scope.delete_article = function(id) {

            x = confirm("Vuoi eliminare questa nota ?")
            if (x == true) {
                $http.get('/tools/campioni/delete_articolo_tot/' + id).then(function(resp) {
                    $scope.deletemsg = resp.data.msg
                    location.reload()
                });


            }

        }




    }
]);