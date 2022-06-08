myapp.controller("new_qrcode_magazzino", [
    "$scope", "$rootScope", "$http",
    function($scope, $rootScope, $http) {
        // create a message 
        console.log('new_qrcode_magazzino');
        $scope.ip = location.host;
        $scope.find_ordine = function(id) {
            $http
                .get("/tools/statomagazzino/find_ordine/" + id)
                .then(function(response) {
                    $scope.selordini = response.data
                });


        }


        $scope.reset = function() {
            delete $scope.modal_select_data;
            delete $scope.selordini;
            delete $scope.dataorder;
            delete $scope.selectedidex;
            delete $scope.generate;
            delete $scope.prep;
            delete $scope.pack;
            delete $scope.aspe;
            delete $scope.spe;
        }





        $scope.generaqrcode = function(index) {
            $scope.selectedidex = index
            let selid = $scope.selordini[index]['id']
            $scope.prep = 'IESample http://' + $scope.ip + '/tools/statomagazzino/stat_mag/' + selid + '/' + 0
            $scope.pack = 'IESample http://' + $scope.ip + '/tools/statomagazzino/stat_mag/' + selid + '/' + 1
            $scope.aspe = 'IESample http://' + $scope.ip + '/tools/statomagazzino/stat_mag/' + selid + '/' + 2
            $scope.spe = 'IESample http://' + $scope.ip + '/tools/statomagazzino/stat_mag/' + selid + '/' + 3
            $("#qrcode").qrcode({
                text: $scope.prep,
                width: 100,
                height: 100,
                colorDark: "#000000",
                colorLight: "#ffffff"
            });
            $("#qrcode1").qrcode({
                text: $scope.pack,
                width: 100,
                height: 100,
                colorDark: "#000000",
                colorLight: "#ffffff"
            });


            $("#qrcode2").qrcode({
                text: $scope.aspe,
                width: 100,
                height: 100,
                colorDark: "#000000",
                colorLight: "#ffffff"
            });



            $("#qrcode3").qrcode({
                text: $scope.spe,
                width: 100,
                height: 100,
                colorDark: "#000000",
                colorLight: "#ffffff"
            });



            $scope.generate = true;






        }









    }
]);