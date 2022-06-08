myapp.controller("stato_ordini_magazzinoController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location", "$timeout",

    function($scope, $rootScope, $http, $routeParams, $location, $timeout) {
        // create a message 
        console.log('stato_ordini_magazzinoController');




        $scope.modview = false;

        $scope.datamodal = function(index) {
            $scope.modal_select_data = $scope.dataorder[index]
            let selid = $scope.modal_select_data['ID']
            $scope.modal_select_data.prep = 'http://192.168.1.205:1111/magazzino/stat_mag/' + selid + '/' + 0
            $scope.modal_select_data.pack = 'http://192.168.1.205:1111/magazzino/stat_mag/' + selid + '/' + 1
            $scope.modal_select_data.aspe = 'http://192.168.1.205:1111/magazzino/stat_mag/' + selid + '/' + 2
            $scope.modal_select_data.spe = 'http://192.168.1.205:1111/magazzino/stat_mag/' + selid + '/' + 3
        }


        $scope.reset = function() {
            delete $scope.modal_select_data;
            delete $scope.selordini;
            delete $scope.dataorder;
            delete $scope.generate
            $scope.$apply()
        }






        $scope.pin = function(pin) {
            if (pin == '5040') {
                $scope.modview = true;
                $('#pinmodal').modal('hide');
            }
        }


        $http
            .get("/tools/statomagazzino/get_all_status")
            .then(function(response) {
                $scope.dataorder = response.data;
            });




        setInterval(function() {
            $scope.timer = 60
            $http
                .get("/tools/statomagazzino/get_all_status")
                .then(function(response) {
                    $scope.dataorder = response.data
                    $scope.modview = false;
                });

        }, 60000)

        $scope.timer = 60
        setInterval(function() {
            $scope.timer -= 1;
            $scope.$apply();

        }, 1000)


        $scope.calc_daydiff = function(a) {
            var y = new Date()
            var a = moment(a);
            var b = moment(y);
            var diffDays = b.diff(a, 'days');
            return diffDays + 1
        }






    }
]);