myapp.controller("articoliController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('articoliController');

        console.log($routeParams.id)

        if ($routeParams.id) {
            if ($routeParams.id == 'new') {
                $scope.action = "new";

                console.log($scope.artico)
                $scope.insert = function(data) {
                    console.log(data);
                    $http.post('articoli/insert', data).then(function(resp) {
                        $scope.msg = resp.data;
                        console.log($scope.msg)


                        if ($scope.msg.message == true) {

                            $location.url('/rs/articoli');
                        } else {


                        }

                    });

                }

            } else {
                $scope.action = "mod";
                console.log($routeParams.id);
                $http.get('/articoli/' + $routeParams.id).then(function(resp) {
                    $scope.articolo = resp.data;
                    console.log($scope.articolo)


                    $scope.modifica = function() {
                        console.log($scope.artico)
                        $http.post('/articoli/update/' + $routeParams.id, $scope.articolo).then(function(resp) {
                            $scope.msg = resp.data;
                            console.log($scope.msg)

                            if ($scope.msg.message == true) {

                                $location.url('/rs/articoli');
                            } else {


                            }
                        });



                    }




                });
            }
        } else {
            $http.get('/articoli').then(function(resp) {
                $scope.articolo = resp.data;
                console.log($scope.articolo)
            });




            $scope.delete = function(el) {

                x = confirm("Sei sicuro di voler eliminare ?")
                console.log(x)

                if (x == true) {

                    $http.get('/articoli/delete/' + el).then(function(resp) {
                        $scope.msg = resp.data;
                        console.log($scope.msg)
                        if ($scope.msg.message == true) {
                            window.location.reload()

                        } else {

                            alert("articolo non Eliminato")

                        }
                    });

                }



            }
        }
    }
]);