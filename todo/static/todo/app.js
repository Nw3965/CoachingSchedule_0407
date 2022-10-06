// CSRF対策
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

document.addEventListener('DOMContentLoaded', function () {

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        // カレンダーの生成とオプションの説明 https://www.mitsue.co.jp/knowledge/blog/frontend/202012/08_0900.html
        editable: true,
        navLinks: true,
        locale: 'ja',
        nowIndicator: true,
        // 日付をクリック、または範囲を選択したイベント
        selectable: true,
        select: function (info) {
            //alert("selected " + info.startStr + " to " + info.endStr);

            // 入力ダイアログ 特定のURLにジャンプ
            window.location.href ='/task/new/';

         
        },

        events: function (info, successCallback, failureCallback) {

            axios
                .post("/list/", {
                    start_date: info.start.valueOf(),
                    end_date: info.end.valueOf(),
                })
                .then((response) => {
                    calendar.removeAllEvents();
                    successCallback(response.data);
                })
                .catch(() => {
                    // バリデーションエラーなど
                    alert("登録に失敗しました");
                });
        },
        // eventClick: function(event) {

        //     //console.dir(event); オブジェクトの中身をチェック。
            
        //     var title = prompt('予定を更新してください:');
            
        //     if(title && title!=""){
        //     event.title = title;
        //     //イベント（予定）の修正
        //     $('#calendar').fullCalendar('updateEvent', event);
        //     }else{
        //     //イベント（予定）の削除  idを指定して削除。
        //     $('#calendar').fullCalendar("removeEvents", event.id);
        //     }
        // }   
        
        eventDrop: function (info) {
            var start = moment(info.event.start).format("Y-MM-DD HH:mm:ss");
            var end = moment(info.event.start).format("Y-MM-DD HH:mm:ss");
            $.ajax({
                url: 'edit-event.php',
                data: { start: start, end: end, id: id },
                type: "POST",
                success: function (response) {
                    displayMessage("Updated Successfully");
                }
            });
        },
        eventDrop: function (info) {
          window.location.href ='/task/' + info.event.id + '/delete/';
            if (deleteMsg) {

            }
        },
        eventClick: function (info) {
          window.location.href ='/task/' + info.event.id + '/';
        },

        const : CustomViewConfig = {
            classNames: ['custom-view'],
            buttonText: '予定リスト',
            duration: {days: 31},
            titleFormat: function (date) {
              const startYear = date.start.year;
              const endYear = date.end.year;
              const startMonth = date.start.month + 1;
              const endMonth = date.end.month + 1;
              const startDay = date.start.day;
              const endDay = date.end.day;
          
              if (startYear === endYear) {
                  return startYear + '年' + startMonth + '月' + startDay + '日 ～ ' + endMonth + '月' + endDay + '日';
              } else {
                  return startYear + '年' + startMonth + '月' + startDay + '日 ～ ' + endYear + '年' + endMonth + '月' + endDay + '日';
              }
            },
            content: function (props) {
              const segs = FullCalendar.sliceEvents(props, true);
              let getData = '';
              function addZero (num) {
                let result = '';
                if (num < 10) {
                  result = '0' + num;
                } else {
                  result = String(num);
                }
          
                return result;
              };
              function getSegs() {
                for (let i = 0, len = segs.length; i < len; i++) {
                  const data = segs[i];
                  const start = data.instance.range.start;
                  const end = data.instance.range.end;
                  const month = start.getMonth() + 1;
                  const day = start.getDate();
                  const weekNum = start.getDay();
                  const week = ['(日)', '(月)', '(火)', '(水)', '(木)', '(金)', '(土)'][weekNum];
                  const getDate = month + '月' + day + '日' + week;
          
                  const startHours = start.getUTCHours();
                  const endHours = end.getUTCHours();
                  const startMinutes = start.getUTCMinutes();
                  const endMinutes = end.getUTCMinutes();
                  let getTime;
                  if (startHours + startMinutes + endHours + endMinutes === 0) {
                    getTime = '終日';
                  } else {
                    getTime = addZero(startHours) + ':' + addZero(startMinutes) + '-' + addZero(endHours) + ':' + addZero(endMinutes);
                  }
          
                  const getEvent = data.def.title;
          
                  getData += '<tr><th>' + getDate + '</th><td>'  + getEvent + '</td></tr>';
                }
                return getData;
              }
              getSegs();
          
              let html;
              if (getData === '') {
                html = '<div class="not-data">表示する予定はありません</div>';
              } else {
                html = '<table><thead><tr><th>日付</th><th>概要</th></tr></thead>' +
                '<tbody>' + getData + '</tbody>' +
                '</table>';
              }
          
              return {html: html};
            }
        },

        views: {
            custom: CustomViewConfig
          },
          headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth,custom'
        },

        eventSources: [
            { //個人のAPIキーだと公開するのは良くないかもしれない。
              googleCalendarApiKey: 'AIzaSyDWQIjf3Vq4-VixK7OBfrVPPMWIoXiFyPI',
              googleCalendarId: 'japanese__ja@holiday.calendar.google.com',
              display: 'background',
            }
          ]
    });

    calendar.render();
});

