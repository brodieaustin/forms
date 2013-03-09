#process a tab or comma separated list of fields into form fields
#order of fields should be:
#field name,field type,label,order
#
class Form:
    def __init__(self, name):
        self.id = name
        self.fields = []

    def make_template(self):
        template = '<form id="' + self.id + '" method="" ' \
                   + ' action="">\n{form}</form>'

        return template

    def get_fields(self):
        return self.fields

    def add_field(self, fname, ftype, flabel, frequired, forder):
        fields = self.get_fields()

        if fname not in fields:
            fields.append(Field(fname, ftype, flabel, frequired, forder))
        else:
            print 'this field already exists!'

    def get_field(self, fname):
        f = self.get_fields()
        return f[fname]

    def process_form_file(self, d, f, sep):
        self.dir = d
        self.file = f
        
        fh = open(d + f, 'r')
        lines = fh.readlines()
        fh.close

        for line in lines:
            l = line.split(sep)
            self.add_field(l[0], l[1], l[2], bool(l[3]), int(l[4].strip()))

        print 'fields added!'

    def print_fields(self):
        fields = self.get_fields()

        for f in fields:
            print f.make_field()

    def export_fields(self):
        fh = open(self.dir + 'export-' + self.file, 'w')
        template = self.make_template()
        text = ''

        fields = self.get_fields()

        for f in fields:
            text = text + f.make_field() + '\n'

        template = template.replace('{form}', text)

        fh.write(template)
        fh.close

        print 'fields exported!'
        

class Field:
    def __init__(self, fname, ftype, flabel, frequired, forder):
        self.id = fname
        self.name = fname
        self.type = ftype
        self.label = flabel
        self.required = frequired
        self.order = forder
        self.strorder = str(forder)

    def format_field(self):
        field = ''
        if self.required == True:
            required = ' class="required"'
        else:
            required = ''
        if self.type == 'text' or self.type == 'radio' or \
           self.type == 'checkbox':
            field = '<input type="' + self.type + '" id="' \
                   + self.id + '" name="' + self.name + '"' \
                   +  required \
                   + ' tabindex="' + self.strorder + '" />'
        elif self.type == 'textarea':
            field = '<textarea id="' + self.id + '" name="' \
                   + self.name + '"' + required \
                   + ' tabindex="' + self.strorder \
                   + '"></textarea>'
        elif self.type == 'select':
            field = '<select id="' + self.id + '" name="' \
                   + self.name + '"' + required \
                   + ' tabindex="' + self.strorder \
                   + '">\n\t\t<option></option>\n\t</select>'
        elif self.type == 'button':
            field = '<input type="' + self.type + '" id="' \
                    + self.id + '" name="' + self.name \
                    + ' value="' + self.label + '" tabindex="' \
                    + self.strorder + '" />'
        elif self.type == 'submit':
            field = '<input type="' + self.type + '"' \
                    + ' value="' + self.label + '" tabindex="' \
                    + self.strorder + '" />'
        else:
            field = '<input type="' + self.type + '" id="' \
                   + self.id + '" name="' + self.name +'"' \
                   + required \
                   + ' tabindex="' + self.strorder + '" />'
        return field

    def make_field(self):
        field = self.format_field()
        required = ' <em>*</em>' if self.required == True else ''
        label = '<div>\n\t'
        if self.type == 'radio' or self.type == 'checkbox':
            label =  label + '<label for="' + self.id + '">' \
                    + field + self.label + required + '</label>'
        elif self.type == 'button' or self.type == 'submit':
            label = label + field
        else:
            label = label + '<label for="' + self.id + '">' \
                   + self.label + required + '</label>\n\t' + field

        label = label + '\n</div>'

        return label
