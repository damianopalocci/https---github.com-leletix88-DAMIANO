myapp.controller("lavorazioneController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('lavorazioneController');


        $scope.insert = true
        $scope.modify = false


        $http.get("/officina/lavorazione/find_all_code").then(function(resp) {
            $scope.all_code = resp.data

            $scope.current_page = $location.path()
            let look_path = $scope.current_page.split('/')
            $scope.current_page = look_path[2]
        });


        $scope.cerca_codice = function(codice) {

            codice = $scope.mycodice

            $http.get("/officina/lavorazione/find_codice/" + codice).then(function(resp) {
                $scope.data_codice = resp.data[0]
                console.log($scope.data_codice)
            });

        }


        $scope.add_codice = function() {

            $http.post('/officina/lavorazione/add_code', $scope.data_codice).then(function(resp) {
                $scope.db_all_art = resp.data.msg
                console.log($scope.db_all_art)
                location.reload()
            });



        }


        $scope.delete_code = function(id) {
            console.log(id)

            x = confirm("Vuoi eliminare questo Utente ?")
            if (x == true) {
                $http.get('/officina/lavorazione/delete_one_code/' + id).then(function(resp) {
                    $scope.deletemsg = resp.data.msg
                    location.reload()
                });

            }

        }



        $scope.update_code = function() {

            $http.post('/officina/lavorazione/update_one_code/' + $scope.one_code._id, $scope.one_code).then(function(resp) {
                $scope.update_respons_code = resp.data.msg;
                location.reload()
            });
        }


        $scope.get_one_code = function(data) {
            $scope.insert = false
            $scope.modify = true
            $scope.one_code = data

        }




    }
]);