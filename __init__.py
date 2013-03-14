#process a yaml-like file with form and field info
#field info should be in csv format
#file should be structured like:
#
#---
#id: id
#subject: subject
#sender: name,email [only 1]
#receiver: name,email [separate multiple with ;]
#---
#field name,field type,label,required[t/f],order
#
#can render form as html and generate json config file
#
import json

class Form:
    def __init__(self):
        self.id = ''
        self.subject = ''
        self.recipients = []
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

    def add_sender(self, sname, semail):
        self.sender = Sender(sname, semail)

    def process_sender(self, line):
        pieces = line.split(',')
        print pieces
        name = pieces[0]
        email = pieces[1]

        self.add_sender(name, email)
        print self.sender

    def get_sender_dict(self):
        s = self.sender
        return s.to_dict()

    def add_recipient(self, rname, remail):
        self.recipients.append(Recipient(rname, remail))

    def process_recipients(self, line):
        pieces = line.split(';')

        for p in pieces:
            temp_piece = p.split(',')
            name = temp_piece[0]
            email = temp_piece[1]
            self.add_recipient(name, email)

    def get_recipients_dict(self):
        recipients = self.recipients
        rs = []
        for r in recipients:
            rs.append(r.to_dict())

        return rs

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
            line = line.strip()
            if line != '---':
                if 'id:' in line:
                    self.id = line[len('id:'):].strip()
                elif 'subject:' in line:
                    self.subject = line[len('subject:'):].strip()
                elif 'sender:' in line:
                    self.process_sender(line[len('sender:'):].strip())
                elif 'recipients' in line:
                    self.process_recipients(line[len('recipients:'):].strip())
                else:
                    l = line.split(sep)
                    self.add_field(l[0], l[1], l[2], bool(l[3]), int(l[4].strip()))

        print 'file processed!'

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

    def get_fields_dict(self):
        fields = self.get_fields()
        fs = {}

        for i in range(0, len(fields)):
            fs[fields[i].name] = fields[i].required

        return fs

    def create_config(self):
        self.config = {}
        self.config['id'] = self.id
        self.config['subject'] = self.subject
        self.config['sender'] = self.get_sender_dict()
        self.config['recipients'] = self.get_recipients_dict()
        self.config['fields'] = self.get_fields_dict()

    def config_to_json(self):
        return json.dumps(self.config, indent=4)

    def export_config(self):
        fh = open(self.dir + 'config.json', 'w')
        json.dump(self.config, fh, indent=4)
        fh.close
        print 'config exported!'

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

    def to_dict(self):
        return {self.name : self.required}

class Sender:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def to_dict(self):
        d = {'name': self.name, 'email': self.email}
        return d

class Recipient:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def to_dict(self):
        d = {'name': self.name, 'email': self.email}
        return d
        
