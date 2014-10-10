(function () {
    var app = angular.module("settings", [ "ngResource" ]);

    app.controller("settingsController", ["$scope", "settingsService", function ($scope, settingsService) {
        var vm = this;

        vm.newSettings = {};

        vm.items = [];

        settingsService.query(function (data) {
            vm.items = data.items;
        });

        vm.Save = function () {
            settingsService.save(vm.newSettings, function (data) {
                vm.items = data.items;
            });
        };

        vm.Delete = function (item) {
            settingsService.del({ name: item.name },
                function (data) {
                    vm.items = data.items;
                });
        };
    }]);

    app.factory("settingsService", ["$resource",
      function ($resource) {
          return $resource("/api/settings", {}, {
              query: { method: "GET", isArray: false, cache: false },
              del: { method: "DELETE" },
              save: { method: "POST" }
          });
      }]);

})();