myapp.controller("new_campioniController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('new_campioniController');


        $scope.articoid = $routeParams.id;

        if ($scope.articoid) {
            $scope.updv = true
            $http.get('/tools/campioni/getcampioni/articolo/' + $scope.articoid).then(function(resp) {
                $scope.db_articolo = resp.data[0]

                $rootScope.current_page = $location.path()
                $rootScope.current_page = $rootScope.current_page.split('/')
                $rootScope.current_page = $rootScope.current_page[1]

            });
            $scope.upload = function() {
                delete $scope.db_articolo._id
                $http.post('/tools/campioni/update/' + $scope.articoid, $scope.db_articolo).then(function(resp) {
                    $scope.addresponse = resp.data.msg
                    if ($scope.addresponse == 200) {
                        history.back();
                    }
                });
            }



        } else {
            $scope.insert = function() {
                $scope.db_articolo['stato'] = 'Nuovo'
                $http.post('/tools/campioni/newcampione', $scope.db_articolo).then(function(resp) {
                    $scope.addresponse = resp.data.msg
                    if ($scope.addresponse == 200) {
                        location.replace('/#!/rs/campioni')

                    }

                });


            }


        }


    }
]);