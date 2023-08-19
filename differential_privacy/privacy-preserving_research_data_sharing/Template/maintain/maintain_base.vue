<!DOCTYPE html>
{% load i18n %}
{% load static %}
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block title %}maintain base{% endblock title %}</title>
        <!-- Core CSS - Include with every page -->
        <link href="{% static 'plugins/vue/vuesax.css' %}" rel="stylesheet" />
        <link href="{% static 'plugins/bootstrap/bootstrap.css' %}" rel="stylesheet" />
        <link href="{% static 'plugins/bootstrap/customfile.css' %}" rel="stylesheet" />
        <link href="{% static 'plugins/bootstrap/typesetting.css' %}" rel="stylesheet" />
        <link href="{% static 'plugins/bootstrap/customselect.css' %}" rel="stylesheet" />
        <link href="{% static 'plugins/bootstrap/spinner.css' %}" rel="stylesheet" />
        <link href="{% static 'font-awesome/css/font-awesome.css' %}" rel="stylesheet" />
        <link href="{% static 'fonts/fonts1.css' %}" rel="stylesheet" />
        <link href="{% static 'css/style.css' %}" rel="stylesheet" />
        <link href="{% static 'css/main-style1.css' %}" rel="stylesheet" />
        <link href="{% static 'css/hint-style.css' %}" rel="stylesheet" />
        <link href="{% static 'css/arrow-style1.css' %}" rel="stylesheet" />
        <link href="{% static 'css/parameter-setting-style.css' %}" rel="stylesheet" />
        <!-- Page-Level CSS -->
        <link href="{% static 'plugins/morris/morris-0.4.3.min.css' %}" rel="stylesheet" />
        
        <!-- Core Scripts - Include with every page -->
        <script src="{% static 'plugins/vue/vue.js' %}"></script>
    	<script src="{% static 'plugins/jquery-3.5.1.min.js' %}"></script>
        <script src="{% static 'plugins/bootstrap/bootstrap.min.js' %}"></script>
        <script src="{% static 'plugins/bootstrap/tooltip.js' %}"></script>
        <script src="{% static 'plugins/metisMenu/jquery.metisMenu.js' %}"></script>
        <!-- Page-Level Plugin Scripts-->
        <script src="{% static 'plugins/morris/raphael-2.1.0.min.js' %}"></script>
        <script src="{% static 'plugins/morris/morris.js' %}"></script>
    </head>
    <style>
        font {
            {% if LANGUAGE_CODE == 'zh-hant' %}
                font-family: Helvetica, "Microsoft JhengHei";
            {% elif LANGUAGE_CODE == 'en-us' %}
                font-family: Avenir;
            {% endif %}
        }

        {% if LANGUAGE_CODE == 'en-us' %}
            .en_little_content{
                font-size: 18px;
            }
        {% endif %}
    </style>
    <body style="color:#000000">
        <!--  wrapper -->
        <div id="wrapper">
            {% include 'maintain/maintain_navbar.html' %}
            <!--  page-wrapper -->
            <div id="page-wrapper" style="margin-top:20px; margin-bottom:40px; min-height:250px;">
                <div style="padding-bottom:20px">
                    <!-- Page Header -->
                    <font class="title_word">[[ title ]]</font>
                    <!--End Page Header -->
                </div>

                <div class="row" style="margin:0px">
                    {% block content %}{% endblock content %}
                </div>
            </div>
            {% include 'footer.html' %}             
        </div>
    </body>
</html>

<script>
    Vue.component('cell', {
        delimiters: ['[[', ']]'],
        props: ['cell_title'],
        template: '\
            <div class="col-lg-12" style="width:100%">\
                <div class="panel panel-primary" style="width:100%">\
                    <div class="panel-heading">\
                        <i class="fa fa-flask fa-fw"></i>[[ cell_title ]]\
                    </div>\
                    <div class="panel-body" style="width:100%">\
                        <slot></slot>\
                    </div>\
                </div>\
            </div>\
        ',
    });
    
    page = new Vue({
        delimiters: ['[[', ']]'],
        el: '#page-wrapper',
        data: {
            title: '',
        },
    });
</script>

<script>
    // https://blog.xuite.net/dizzy03/murmur/60259945-%5BJavascript%5D%5B%E8%BD%89%5D+%E7%94%A8JavaScript%E7%99%BC%E5%87%BAPost+Request
    function post_to_url(path, params) {
        // The rest of this code assumes you are not using a library.
        // It can be made less wordy if you use one.
        var form = document.createElement("form");
        form.setAttribute("method", "POST");
        form.setAttribute("action", path);

        var hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        hiddenField.setAttribute("name", "csrfmiddlewaretoken");
        hiddenField.setAttribute("value", "{{ csrf_token }}");
        form.appendChild(hiddenField);
        
        for(var key in params) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);
            form.appendChild(hiddenField);
        }

        document.body.appendChild(form);    // Not entirely sure if this is necessary
        form.submit();
    }
    
    function maintain() {
        warning_alert("{% trans '伺服器維護中' %}")
    }
    
    function hint_click(element_id, hint_level) {
        var target_page = $('#'+element_id+'_page');
        var same_level_element = $("font[name='hint_level_"+hint_level+"']");
        var same_level_page = $("div[name='level_"+hint_level+"_page']");
        var is_close = target_page.is(':hidden');
        
        same_level_page.hide();
        
        if (is_close) {
            target_page.toggle();
        }
        
        same_level_element.each(function() {
            var temp = $(this).html();
            temp = temp.split(' ');
            temp.pop();
            var mapping_page = $('#'+$(this).attr('id')+'_page');
            if (mapping_page.is(':visible')) {
                temp.push('▲');
            } else {
                temp.push('▼');
            }
            $(this).html(temp.join(' '));
        });
    }
</script>
{% block script %}{% endblock script %}
