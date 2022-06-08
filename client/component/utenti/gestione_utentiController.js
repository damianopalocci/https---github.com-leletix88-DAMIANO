myapp.controller("gestione_utentiController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location", "$timeout",

    function($scope, $rootScope, $http, $routeParams, $location, $timeout) {
        // create a message 
        console.log('gestione_utentiController');

        $scope.insert = true
        $scope.modify = false


        $http.get("/utenti/find_all_user").then(function(resp) {
            $scope.all_user = resp.data
        });



        $scope.deleteuser = function(id) {
            console.log(id)

            x = confirm("Vuoi eliminare questo Utente ?")
            if (x == true) {
                $http.get('/utenti/delete_one_user/' + id).then(function(resp) {
                    $scope.deletemsg = resp.data.msg
                    location.reload()
                });

            }

        }



        $scope.adduser = function() {

            /*             $scope.db_preventivo.relid = $scope.db_articolo._id
                        $scope.db_preventivo.user_login_prev = $rootScope.login_info.username */

            $http.post('/utenti/add_user', $scope.one_user).then(function(resp) {
                $scope.db_user = resp.data.msg
                location.reload()
            });



        }


        $scope.updateuser = function() {

            console.log($scope.one_user._id)

            $http.post('/utenti/update_one_user/' + $scope.one_user._id, $scope.one_user).then(function(resp) {
                $scope.update_respons_user = resp.data.msg;
                location.reload()
            });
        }



        $scope.get_one_user = function(data) {
            $scope.insert = false
            $scope.modify = true
            $scope.one_user = data

        }

        $scope.button_user = function() {

            $scope.insert = true
            $scope.modify = false
            $scope.one_user = {}
        }

    }
]);