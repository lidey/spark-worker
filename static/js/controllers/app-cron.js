'use strict';

/* Controllers */

app.controller('AppCronCtrl', ['$scope', '$modalInstance', 'cron', function ($scope, $modalInstance, cron) {

    $scope.cancel = function () {
        $modalInstance.dismiss();
    };

    $scope.type = {
        second: 'wildcard',
        minute: 'wildcard',
        hour: 'wildcard',
        day: 'wildcard',
        month: 'wildcard',
        week: 'wildcard',
        year: 'wildcard'
    };
    $scope.cron = {
        second: '*',
        minute: '*',
        hour: '*',
        day: '*',
        month: '*',
        week: '*',
        year: '*'
    };
    $scope.cycle = {
        second_start: 1, second_end: 2,
        minute_start: 1, minute_end: 2,
        hour_start: 1, hour_end: 2,
        day_start: 1, day_end: 2,
        month_start: 1, month_end: 2,
        week_start: 1, week_end: 2,
        year_start: 2016, year_end: 2050
    };
    $scope.interval = {
        second_start: 0, second_end: 1,
        minute_start: 0, minute_end: 1,
        hour_start: 0, hour_end: 1,
        day_start: 1, day_end: 1,
        month_start: 1, month_end: 1,
        week_start: 1, week_end: 1,
    };
    $scope.work = {
        day_work: 1
    };
    $scope.last = {
        week_last: 1
    };
    $scope.appoint = {seconds: [], minutes: [], hours: [], days: [], months: [], weeks: []};

    function padNumber(num, fill) {
        var len = ('' + num).length;
        return (Array(
            fill > len ? fill - len + 1 || 0 : 0
        ).join(0) + num);
    }

    $scope.second_tab = []
    for (var i = 1; i < 60; i++)
        $scope.second_tab.push({name: padNumber(i, 2), value: String(i)});

    $scope.select_second = function () {
        switch ($scope.type.second) {
            case 'wildcard':
                $scope.cron.second = '*';
                break;
            case 'cycle':
                $scope.cron.second = $scope.cycle.second_start + '-' + $scope.cycle.second_end;
                break;
            case 'interval':
                $scope.cron.second = $scope.interval.second_start + '/' + $scope.interval.second_end;
                break;
            case 'appoint':
                if ($scope.appoint.seconds.length > 0)
                    $scope.cron.second = $scope.appoint.seconds.join(',');
                else
                    $scope.cron.second = '?';
                break;
        }
    };

    $scope.analysis_second = function (second) {
        if (second.indexOf('*') != -1) {
            $scope.type.second = 'wildcard';
        } else if (second.indexOf('-') != -1) {
            $scope.type.second = 'cycle';
            $scope.cycle.second_start = second.split('-')[0];
            $scope.cycle.second_end = second.split('-')[1];
        } else if (second.indexOf('/') != -1) {
            $scope.type.second = 'interval';
            $scope.interval.second_start = second.split('/')[0];
            $scope.interval.second_end = second.split('/')[1];
        } else {
            $scope.type.second = 'appoint';
            $scope.appoint.seconds = second.split(',');
        }
    };

    $scope.minute_tab = []
    for (var i = 1; i < 60; i++)
        $scope.minute_tab.push({name: padNumber(i, 2), value: String(i)});

    $scope.select_minute = function () {
        switch ($scope.type.minute) {
            case 'wildcard':
                $scope.cron.minute = '*';
                break;
            case 'cycle':
                $scope.cron.minute = $scope.cycle.minute_start + '-' + $scope.cycle.minute_end;
                break;
            case 'interval':
                $scope.cron.minute = $scope.interval.minute_start + '/' + $scope.interval.minute_end;
                break;
            case 'appoint':
                if ($scope.appoint.minutes.length > 0)
                    $scope.cron.minute = $scope.appoint.minutes.join(',');
                else
                    $scope.cron.minute = '?';
                break;
        }
    };

    $scope.analysis_minute = function (minute) {
        if (minute.indexOf('*') != -1) {
            $scope.type.minute = 'wildcard';
        } else if (minute.indexOf('-') != -1) {
            $scope.type.minute = 'cycle';
            $scope.cycle.minute_start = minute.split('-')[0];
            $scope.cycle.minute_end = minute.split('-')[1];
        } else if (minute.indexOf('/') != -1) {
            $scope.type.minute = 'interval';
            $scope.interval.minute_start = minute.split('/')[0];
            $scope.interval.minute_end = minute.split('/')[1];
        } else {
            $scope.type.minute = 'appoint';
            $scope.appoint.minutes = minute.split(',');
        }
    };

    $scope.hour_tab = []
    for (var i = 0; i < 24; i++)
        $scope.hour_tab.push({name: padNumber(i, 2), value: String(i)});

    $scope.select_hour = function () {
        switch ($scope.type.hour) {
            case 'wildcard':
                $scope.cron.hour = '*';
                break;
            case 'cycle':
                $scope.cron.hour = $scope.cycle.hour_start + '-' + $scope.cycle.hour_end;
                break;
            case 'interval':
                $scope.cron.hour = $scope.interval.hour_start + '/' + $scope.interval.hour_end;
                break;
            case 'appoint':
                if ($scope.appoint.hours.length > 0)
                    $scope.cron.hour = $scope.appoint.hours.join(',');
                else
                    $scope.cron.hour = '?';
                break;
        }
    };

    $scope.analysis_hour = function (hour) {
        if (hour.indexOf('*') != -1) {
            $scope.type.hour = 'wildcard';
        } else if (hour.indexOf('-') != -1) {
            $scope.type.hour = 'cycle';
            $scope.cycle.hour_start = hour.split('-')[0];
            $scope.cycle.hour_end = hour.split('-')[1];
        } else if (hour.indexOf('/') != -1) {
            $scope.type.hour = 'interval';
            $scope.interval.hour_start = hour.split('/')[0];
            $scope.interval.hour_end = hour.split('/')[1];
        } else {
            $scope.type.hour = 'appoint';
            $scope.appoint.hours = hour.split(',');
        }
    };

    $scope.day_tab = []
    for (var i = 0; i <= 31; i++)
        $scope.day_tab.push({name: padNumber(i, 2), value: String(i)});

    $scope.select_day = function () {
        switch ($scope.type.day) {
            case 'wildcard':
                $scope.cron.day = '*';
                break;
            case 'cycle':
                $scope.cron.day = $scope.cycle.day_start + '-' + $scope.cycle.day_end;
                break;
            case 'interval':
                $scope.cron.day = $scope.interval.day_start + '/' + $scope.interval.day_end;
                break;
            case 'work':
                $scope.cron.day = $scope.work.day_work + 'W';
                break;
            case 'last':
                $scope.cron.day = 'last';
                break;
            case 'appoint':
                if ($scope.appoint.days.length > 0)
                    $scope.cron.day = $scope.appoint.days.join(',');
                else
                    $scope.cron.day = '?';
                break;
        }
    };

    $scope.analysis_day = function (day) {
        if (day.indexOf('*') != -1) {
            $scope.type.day = 'wildcard';
        } else if (day.indexOf('-') != -1) {
            $scope.type.day = 'cycle';
            $scope.cycle.day_start = day.split('-')[0];
            $scope.cycle.day_end = day.split('-')[1];
        } else if (day.indexOf('/') != -1) {
            $scope.type.day = 'interval';
            $scope.interval.day_start = day.split('/')[0];
            $scope.interval.day_end = day.split('/')[1];
        } else if (day.indexOf('last') != -1) {
            $scope.type.day = 'last';
        } else {
            $scope.type.day = 'appoint';
            $scope.appoint.days = day.split(',');
        }
    };

    $scope.month_tab = []
    for (var i = 1; i <= 12; i++)
        $scope.month_tab.push({name: padNumber(i, 2), value: String(i)});

    $scope.select_month = function () {
        switch ($scope.type.month) {
            case 'wildcard':
                $scope.cron.month = '*';
                break;
            case 'cycle':
                $scope.cron.month = $scope.cycle.month_start + '-' + $scope.cycle.month_end;
                break;
            case 'interval':
                $scope.cron.month = $scope.interval.month_start + '/' + $scope.interval.month_end;
                break;
            case 'appoint':
                if ($scope.appoint.months.length > 0)
                    $scope.cron.month = $scope.appoint.months.join(',');
                else
                    $scope.cron.month = '?';
                break;
        }
    };

    $scope.analysis_month = function (month) {
        if (month.indexOf('*') != -1) {
            $scope.type.month = 'wildcard';
        } else if (month.indexOf('-') != -1) {
            $scope.type.month = 'cycle';
            $scope.cycle.month_start = month.split('-')[0];
            $scope.cycle.month_end = month.split('-')[1];
        } else if (month.indexOf('/') != -1) {
            $scope.type.month = 'interval';
            $scope.interval.month_start = month.split('/')[0];
            $scope.interval.month_end = month.split('/')[1];
        } else {
            $scope.type.month = 'appoint';
            $scope.appoint.months = month.split(',');
        }
    };

    $scope.week_tab = []
    for (var i = 1; i <= 7; i++)
        $scope.week_tab.push({name: i, value: String(i)});

    $scope.select_week = function () {
        switch ($scope.type.week) {
            case 'wildcard':
                $scope.cron.week = '*';
                break;
            case 'cycle':
                $scope.cron.week = $scope.cycle.week_start + '-' + $scope.cycle.week_end;
                break;
            case 'interval':
                $scope.cron.week = $scope.interval.week_start + '/' + $scope.interval.week_end;
                break;
            case 'last':
                $scope.cron.week = $scope.last.week_last + 'L';
                break;
            case 'appoint':
                if ($scope.appoint.weeks.length > 0)
                    $scope.cron.week = $scope.appoint.weeks.join(',');
                else
                    $scope.cron.week = '?';
                break;
        }
    };

    $scope.analysis_week = function (week) {
        if (week.indexOf('*') != -1) {
            $scope.type.week = 'wildcard';
        } else if (week.indexOf('-') != -1) {
            $scope.type.week = 'cycle';
            $scope.cycle.week_start = week.split('-')[0];
            $scope.cycle.week_end = week.split('-')[1];
        } else if (week.indexOf('/') != -1) {
            $scope.type.week = 'interval';
            $scope.interval.week_start = week.split('/')[0];
            $scope.interval.week_end = week.split('/')[1];
        } else if (week.indexOf('L') != -1) {
            $scope.type.week = 'last';
            $scope.last.week_last = week.replace('L', '');
        } else {
            $scope.type.week = 'appoint';
            $scope.appoint.weeks = week.split(',');
        }
    };

    $scope.select_year = function () {
        switch ($scope.type.year) {
            //case 'empty':
            //    $scope.cron.year = '';
            //    break;
            case 'wildcard':
                $scope.cron.year = '*';
                break;
            case 'cycle':
                $scope.cron.year = $scope.cycle.year_start + '-' + $scope.cycle.year_end;
                break;
        }
    };

    $scope.analysis_year = function (year) {
        if (year.indexOf('*') != -1) {
            $scope.type.year = 'wildcard';
        } else if (year.indexOf('-') != -1) {
            $scope.type.year = 'cycle';
            $scope.cycle.year_start = year.split('-')[0];
            $scope.cycle.year_end = year.split('-')[1];
        } else {
            //$scope.type.year = 'empty';
        }
    };

    if (cron != undefined && cron != null && typeof(cron) == 'object') {
        $scope.cron = cron;
        $scope.analysis_second(cron.second);
        $scope.analysis_minute(cron.minute);
        $scope.analysis_hour(cron.hour);
        $scope.analysis_day(cron.day);
        $scope.analysis_month(cron.month);
        $scope.analysis_week(cron.week);
        $scope.analysis_year(cron.year);
    }

    $scope.save_cron = function () {
        $modalInstance.close($scope.cron);
    }

}]);