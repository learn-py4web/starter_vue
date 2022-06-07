// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        edit_mode: false,
        add_mode: false,
        isActive: 'classes',
        add_class_name: "",
        add_class_type: "",
        add_instructor_name: "",
        add_instructor_email: "",
        rows: [],
        rows_i: [],
        rows_changes: {},
        rows_i_changes: {}
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => { e._idx = k++; });
        return a;
    };

    app.decorate = (a) => {
        a.map((e) => {
            e._state = { name: "clean", email: "clean", class_name: "clean", class_type: "clean", quarter_1: "clean", quarter_2: "clean", quarter_3: "clean", summer_1: "clean", summer_2: "clean", course_time_sections: "clean", actual_times: "clean" };
            e._server_vals = {name: e.name, email: e.email, class_name: e.class_name, class_type: e.class_type, quarter_1: e.quarter_1, quarter_2: e.quarter_2, quarter_3: e.quarter_3, summer_1: e.summer_1, summer_2: e.summer_2, course_time_sections: e.course_time_sections, actual_times: e.actual_times };
        });
        return a;
    };

    app.add_class = function () {
        axios.post(add_class_url,
            {
                class_name: app.vue.add_class_name,
                class_type: app.vue.add_class_type,
                quarter_1: app.vue.add_quarter_1,
                quarter_2: app.vue.add_quarter_2,
                quarter_3: app.vue.add_quarter_3,
                summer_1: app.vue.add_summer_1,
                summer_2: app.vue.add_summer_2,
                course_time_sections: app.vue.add_course_time_sections,
                actual_times: app.vue.add_actual_times,
                _state: { class_name: "clean", class_type: "clean", quarter_1: "clean", quarter_2: "clean", quarter_3: "clean", summer_1: "clean", summer_2: "clean", course_time_sections: "clean", actual_times: "clean" },
            }).then(function (response) {
                app.vue.rows.push({
                    id: response.data.id,
                    class_name: app.vue.add_class_name,
                    class_type: app.vue.add_class_type,
                    quarter_1: app.vue.add_quarter_1,
                    quarter_2: app.vue.add_quarter_2,
                    quarter_3: app.vue.add_quarter_3,
                    summer_1: app.vue.add_summer_1,
                    summer_2: app.vue.add_summer_2,
                    course_time_sections: app.vue.add_course_time_sections,
                    actual_times: app.vue.add_actual_times,
                    _state: { class_name: "clean", class_type: "clean", quarter_1: "clean", quarter_2: "clean", quarter_3: "clean", summer_1: "clean", summer_2: "clean", course_time_sections: "clean", actual_times: "clean" },

                    _server_vals: {
                        class_name: app.vue.add_class_name,
                        class_type: app.vue.add_class_type,
                        quarter_1: app.vue.add_quarter_1,
                        quarter_2: app.vue.add_quarter_2,
                        quarter_3: app.vue.add_quarter_3,
                        summer_1: app.vue.add_summer_1,
                        summer_2: app.vue.add_summer_2,
                        course_time_sections: app.vue.add_course_time_sections,
                        actual_times: app.vue.add_actual_times
                    }
                });
                app.enumerate(app.vue.rows);
                app.reset_form();
                app.set_add_status(false);
            });
    };

    app.add_instructor = function () {
        axios.post(add_instructor_url,
            {
                name: app.vue.add_instructor_name,
                email: app.vue.add_instructor_email,
                quarter_1: app.vue.add_quarter_1,
                quarter_2: app.vue.add_quarter_2,
                quarter_3: app.vue.add_quarter_3,
                summer_1: app.vue.add_summer_1,
                summer_2: app.vue.add_summer_2,
                _state: { name: "clean", email: "clean", quarter_1: "clean", quarter_2: "clean", quarter_3: "clean", summer_1: "clean", summer_2: "clean", course_time_sections: "clean", actual_times: "clean" },
            }).then(function (response) {
                app.vue.rows_i.push({
                    id: response.data.id,
                    name: app.vue.add_instructor_name,
                    email: app.vue.add_instructor_email,
                    // class_type: app.vue.add_class_type,
                    quarter_1: app.vue.add_quarter_1,
                    quarter_2: app.vue.add_quarter_2,
                    quarter_3: app.vue.add_quarter_3,
                    summer_1: app.vue.add_summer_1,
                    summer_2: app.vue.add_summer_2,
                    _state: { name: "clean", email: "clean", quarter_1: "clean", quarter_2: "clean", quarter_3: "clean", summer_1: "clean", summer_2: "clean", course_time_sections: "clean", actual_times: "clean" },

                    _server_vals: {
                        name: app.vue.add_instructor_name,
                        email: app.vue.add_instructor_email,
                        quarter_1: app.vue.add_quarter_1,
                        quarter_2: app.vue.add_quarter_2,
                        quarter_3: app.vue.add_quarter_3,
                        summer_1: app.vue.add_summer_1,
                        summer_2: app.vue.add_summer_2,
                    }
                });
                app.enumerate(app.vue.rows_i);
                app.reset_form();
                app.set_add_status(false);
            });
    };


    app.reset_form = function () {
        class_name: app.vue.add_class_name="";
        class_type: app.vue.add_class_type="";
        quarter_1: app.vue.add_quarter_1="";
        quarter_2: app.vue.add_quarter_2="";
        quarter_3: app.vue.add_quarter_3="";
        summer_1: app.vue.add_summer_1="";
        summer_2: app.vue.add_summer_2="";
        course_time_sections: app.vue.add_course_time_sections="";
        actual_times: app.vue.add_actual_times="";
    };

    app.delete_class = function (row_idx) {
        let id = app.vue.rows[row_idx].id;
        axios.get(delete_class_url, { params: { id: id } }).then(function (response) {
            for (let i = 0; i < app.vue.rows.length; i++) {
                if (app.vue.rows[i].id === id) {
                    app.vue.rows.splice(i, 1);
                    app.enumerate(app.vue.rows);
                    break;
                }
            }
        });
    };

    app.set_add_status = function (new_status) {
        app.vue.add_mode = new_status;
    };
    
    app.toggle_edit_mode = function() {
        app.vue.edit_mode = !app.vue.edit_mode;
    };

    app.start_edit = function (table, row_idx, fn) {
        if (app.vue.edit_mode) {
            table = (table == app.data.rows ? app.vue.rows : app.vue.rows_i);
            table[row_idx]._state[fn] = "edit";
        }
    };

    app.stop_edit = function (table_view, row_idx, fn) {
        table = (table_view == app.data.rows ? app.vue.rows : app.vue.rows_i);
        table_changes = (table_view == app.data.rows ? app.data.rows_changes : app.data.rows_i_changes);

        let row = table[row_idx];
        if (row._state[fn] === 'edit') {  // if editing
            if (row._server_vals[fn] !== row[fn]) {  // and a change has been made
                // make record of change
                table_changes[row_idx] = {
                    'table': (table_view == app.data.rows ? 'classes' : 'instr'),
                    'id': row.id,
                    'key': fn,
                    'value': row[fn],
                };
                // TODO: change to some other visual indicator
                row._state[fn] = "edit";
            } else {
                row._state[fn] = "clean";
                // remove record of change
                delete table_changes[row_idx];
            }
        }
        // console.log(table_changes);
    };

    app.cancel_edits = function() {
        app.cancel_edit(app.data.rows);
        app.cancel_edit(app.data.rows_i);

        // Exit edit mode
        app.toggle_edit_mode();
    }

    app.clear_changes_logs = function() {
        // clear changes dicts
        for (const key in app.data.rows_changes) {
            delete app.data.rows_changes[key];
        }
        for (const key in app.data.rows_i_changes) {
            delete app.data.rows_i_changes[key];
        }
    };

    app.cancel_edit = function(table) {
        let entries = ['class_name', 'class_type', 'quarter_1', 'quarter_2', 'quarter_3', 'summer_1', 'summer_2', 'course_time_sections', 'actual_times'];
        // Reset table to current server values
        table = (table == app.data.rows ? app.vue.rows : app.vue.rows_i);
        for (let i = 0; i < table.length; ++i) {
            let row = table[i];
            for (const [key, value] of Object.entries(row)) {
                if (entries.includes(key) && row._server_vals[key] !== value) {
                    row[key] = row._server_vals[key];
                    row._state[key] = "clean";
                }
              }
        }
        app.clear_changes_logs();    
    };

    app.edit_classes = function() {
        axios.get(edit_classes_url);
    };

    // TODO: update vue for 'instructors' tab
    app.save_table_changes = function() {
        // Update db and vue
        app.update_table(app.data.rows);
        app.update_table(app.data.rows_i);

        // clear change logs
        app.clear_changes_logs();

        // Exit Edit Mode
        app.toggle_edit_mode();
    };

    app.update_table = function(table_view) {
        let entries = ['name', 'email', 'class_name', 'class_type', 'quarter_1', 'quarter_2', 'quarter_3', 'summer_1', 'summer_2', 'course_time_sections', 'actual_times'];
        
        table = (table_view == app.data.rows ? app.vue.rows : app.vue.rows_i);
        func = (table_view == app.data.rows ? edit_class_url : edit_instructor_url);
        table_changes = (table_view == app.data.rows ? app.data.rows_changes : app.data.rows_i_changes);
        console.log(table_changes);
        for (const row_idx in table_changes) {
            console.log('row_idx: ', row_idx, 'row: ', table_changes[row_idx]);            
        }
        // update db only if there are changes
        if (Object.keys(table_changes).length > 0) {

            for (const row_idx in table_changes) {
                // console.log('row_idx: ', row_idx, 'row: ', table_changes[row_idx]);
                field = table_changes[row_idx]['key'];
                table[row_idx]._state[field] = 'pending';                
            }

            axios.post(update_tables_url, {
                changes_list: table_changes
            }).then(function (result) {
                // putting the loop here doesnt work
            });
            // update vue
            for (const row_idx in table_changes) {
                // table[row_idx][table_changes[row_idx]] = table_changes[row];
                field = table_changes[row_idx]['key'];
                value = table_changes[row_idx]['value'];
                
                // update current table/tab
                table[row_idx]._server_vals[field] = value;
                table[row_idx][field] = value;
                table[row_idx]._state[field] = 'clean';

                // update other table/tab
            }
        }
    }

    // We form the dictionary of all methods, so we can assign them
    // to the Vue app in a single blow.
    app.methods = {
        toggle_edit_mode: app.toggle_edit_mode,
        save_table_changes: app.save_table_changes,
        update_table: app.update_table,
        add_class: app.add_class,
        add_instructor: app.add_instructor,
        set_add_status: app.set_add_status,
        delete_class: app.delete_class,
        start_edit: app.start_edit,
        stop_edit: app.stop_edit,
        edit_classes: app.edit_classes,
        cancel_edit: app.cancel_edit,
        cancel_edits: app.cancel_edits,
        clear_changes_logs: app.clear_changes_logs
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    // Generally, this will be a network call to the server to
    // load the data.
    // For the moment, we 'load' the data from a string.
    app.init = () => {
        axios.get(load_classes_url).then(function (response) {
            app.vue.rows = app.decorate(app.enumerate(response.data.rows));
        });

        axios.get(load_instructors_url).then(function (response) {
            app.vue.rows_i = app.decorate(app.enumerate(response.data.rows));
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);