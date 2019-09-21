import tkinter
from tkinter import messagebox
import re
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import corpus
import letter
import numpy as np
import pickle

def pickle_corpus():
    letter_corp = corpus.Corpus([])
    with open('letters.json', encoding='utf8') as f:
        letter_list = json.load(f)
    for i, l in enumerate(letter_list):
        l_obj = letter.Letter(l['writer'], l['addressee'], int(l['year']), l['language'], l['text'], i)
        letter_corp.add_letter(l_obj)
        letter_corp.add_writer(l['writer'].lower())
        letter_corp.add_addressee(l['addressee'].lower())
        letter_corp.add_year(int(l['year']))
    letter_corp.compute_total_word_count()
    with open('corpus.pickle', 'wb') as f:
        pickle.dump(letter_corp, f)

def load_corpus():
    print('Loading corpus')
    with open('corpus.pickle', 'rb') as fin:
        letter_corp = pickle.load(fin)
    print('Finished loading')
    return letter_corp

# def draw_bar_graph(counts_by_category, category, count_type):
#     categories, freqs = zip(*counts_by_category)
#     r = tkinter.Tk()
#     r.title('Bar Chart')
#     x_locs = np.arange(len(categories))
#     bar_heights = list(freqs)
#     fig = Figure()
#     ax = fig.add_subplot(111)
#     bars = ax.bar(x_locs, bar_heights, color='b')
#     ax.set_ylabel('{0} Frequency'.format(count_type.title()))
#     ax.set_title('{0} Frequency by {1}'.format(count_type.title(), category.title()))
#     ax.set_xticks(x_locs)
#     ax.set_xticklabels(list(categories), rotation='vertical')
#     plt.margins(0.2)
#     fig.subplots_adjust(bottom=0.15)
#     for b in bars:
#         height = b.get_height()
#         ax.annotate('{}'.format(height), xy=(b.get_x() + b.get_width() / 2, height), xytext=(0, 3),
#                     textcoords='offset points', ha='center', va='bottom')
#
#     manager = plt.get_current_fig_manager()
#     manager.resize(*manager.window.maxsize())
#     canvas = FigureCanvasTkAgg(fig, master=r)
#     canvas.draw()
#     canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#     tkinter.mainloop()

def show_concordances(concordance_lines, term):
    r = tkinter.Tk()
    r.title("Concordance Results")
    # r.attributes('-fullscreen', True)
    text_frame = tkinter.Frame(r)
    text_frame.pack()
    right_scrollbar = tkinter.Scrollbar(text_frame)
    right_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    bottom_scrollbar = tkinter.Scrollbar(text_frame, orient=tkinter.HORIZONTAL)
    bottom_scrollbar.pack(side=tkinter.BOTTOM, fill=tkinter.X, anchor=tkinter.W)
    text_box = tkinter.Text(text_frame, wrap='none', width=300, yscrollcommand=right_scrollbar.set, xscrollcommand=bottom_scrollbar.set)
    text_box.pack()
    right_scrollbar.config(command=text_box.yview)
    bottom_scrollbar.config(command=text_box.xview)
    if len(concordance_lines) == 0:
        text_box.insert(tkinter.END, 'No results found for {0}'.format(term))
    for line in concordance_lines:
        text_box.insert(tkinter.END, line)
    r.mainloop()

def concordance_to_file(concordance_lines):
    file = filename.get()
    if file == '':
        messagebox.showerror('Error', 'Please enter the name of the file to write to.')
        return
    with open(file, 'w') as f:
        for line in concordance_lines:
            f.write(line)
            f.write('\n')
    messagebox.showinfo('Success', 'Concordances written to {}'.format(file))

def show_counts(raw, norm):
    r = tkinter.Tk()
    r.title("Frequency Results")
    text_frame = tkinter.Frame(r)
    text_frame.pack()
    text_box = tkinter.Text(text_frame)
    text_box.pack()
    text_box.insert(tkinter.END, 'Raw frequency:\t{0}\n'.format(raw))
    text_box.insert(tkinter.END, 'Normalized frequency per 1000 words:\t{0}'.format(norm))
    r.mainloop()

def counts_to_file(raw, norm):
    file = filename.get()
    if file == '':
        messagebox.showerror('Error', 'Please enter the name of the file to write to.')
        return
    with open(file, 'w') as f:
        f.write('Raw frequency:\t{0}\n'.format(raw))
        f.write('Normalized frequency per 1000 words:\t{0}'.format(norm))
    messagebox.showinfo('Success', 'Frequencies written to {}'.format(file))

def show_by_category(counts_by_category, cat, freq_type):
    categories, freqs = zip(*counts_by_category)
    r = tkinter.Tk()
    r.title('Bar Chart')
    scroll = tkinter.Scrollbar(r)
    scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    x_locs = np.arange(len(categories))
    bar_heights = list(freqs)
    fig = Figure(figsize=(15, 11))
    # plt.margins(0.2)
    # fig.tight_layout()
    fig.subplots_adjust(bottom=0.4)
    ax = fig.add_subplot(111)
    bars = ax.bar(x_locs, bar_heights, color='b')
    ax.set_ylabel('{0} Frequency'.format(freq_type.title()))
    ax.set_title('{0} Frequency by {1}'.format(freq_type.title(), cat.title()))
    ax.set_xticks(x_locs)
    ax.set_xticklabels(list(categories), rotation='vertical')

    for b in bars:
        height = b.get_height()
        ax.annotate('{}'.format(height), xy=(b.get_x() + b.get_width() / 2, height), xytext=(0, 3),
                    textcoords='offset points', ha='center', va='bottom')

    canvas = FigureCanvasTkAgg(fig, master=r)
    canvas.draw()
    canvas.get_tk_widget().config(yscrollcommand=scroll.set)
    scroll.config(command=canvas.get_tk_widget().yview)
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    while True:
        try:
            r.mainloop()
        except UnicodeDecodeError:
            continue
        break

def categories_to_file(counts_by_category, cat, freq_type):
    file = filename.get()
    if file == '':
        messagebox.showerror('Error', 'Please enter the name of the file to write to.')
        return
    with open(file, 'w') as f:
        f.write('{0}\t{1}\n'.format(cat, freq_type))
        for c, f in counts_by_category:
            f.write('{0}\t{1}\n'.format(c, f))
    messagebox.showinfo('Success', 'Frequencies by category written to {}'.format(file))

def words_to_regex(words):
    words = re.sub('\s+', '\s+', words)
    words = '\s+{0}\s+'.format(words)
    return words

def search():
    corp = whole_corp
    term = search_term.get()
    is_sensitive = sensitive.get()
    write_to_file = to_file.get()
    if term == '':
        messagebox.showerror('Error', 'No search term was entered. Please try again.')
        return
    if not is_regex.get():
        term = words_to_regex(term)
    if output_type.get() == 'concordance':
        concordance_lines = corp.get_concordances(term, is_sensitive, context_len.get())
        if write_to_file:
            concordance_to_file(concordance_lines)
        else:
            show_concordances(concordance_lines, term)
    elif output_type.get() == 'total frequency':
        raw = corp.get_total_raw_count(term, is_sensitive)
        norm = corp.get_normalized_count(raw)
        if write_to_file:
            counts_to_file(raw, norm)
        else:
            show_counts(raw, norm)
    else:
        cat = category.get()
        freq_type = frequency_type.get()
        print('Getting counts by category')
        counts_by_category = corp.get_counts_by_category(term, is_sensitive, cat, freq_type)
        if write_to_file:
            categories_to_file(counts_by_category)
        else:
            show_by_category(counts_by_category, cat, freq_type)


def toggle_suboptions():
    if output_type.get() == 'frequency by category':
        suboption_frame.grid()
        conc_option_frame.grid_remove()
    elif output_type.get() == 'concordance':
        conc_option_frame.grid()
        suboption_frame.grid_remove()
    else:
        suboption_frame.grid_remove()
        conc_option_frame.grid_remove()

def toggle_file_entry():
    if to_file.get():
        file_label.grid()
        file_entry.grid()
    else:
        file_label.grid_remove()
        file_entry.grid_remove()

def toggle_writer_filter():
    if by_writer.get():
        writer_frame.grid()
    else:
        writer_frame.grid_remove()

def toggle_recipient_filter():
    if by_recipient.get():
        recipient_frame.grid()
    else:
        recipient_frame.grid_remove()

def toggle_year_filter():
    if by_year.get():
        year_frame.grid()
    else:
        year_frame.grid_remove()


plt.switch_backend('TkAgg')
whole_corp = load_corpus()

# show_concordances(whole_corp, '\sopera\s', False, 20)
# show_counts(whole_corp, '\sopera\s', False)
# show_by_category(whole_corp, '\sopera\s', False, 'year', 'raw')

# After writing command functions remove quotes from around name of commands
root = tkinter.Tk()
root.title('Queen Victoria Corpus')

# All widgets and subframes go in this frame
all_content = tkinter.Frame(root)
welcome = tkinter.Label(all_content, text='Welcome to the Queen Victoria Correspondence Corpus!')

# Set up search term entry frame
entry_frame = tkinter.Frame(all_content)
entry_label = tkinter.Label(entry_frame, text='Enter a search term:')
search_term = tkinter.StringVar()
search_entry = tkinter.Entry(entry_frame, textvariable=search_term)
# Set up search term options frame
options_frame = tkinter.Frame(entry_frame)
options_label = tkinter.Label(options_frame, text='Search term options')
sensitive = tkinter.BooleanVar()
sensitive.set(False)
is_regex = tkinter.BooleanVar()
is_regex.set(False)
case_R1 = tkinter.Radiobutton(options_frame, text="Case insensitive", variable=sensitive, value=False)
case_R2 = tkinter.Radiobutton(options_frame, text="Case sensitive", variable=sensitive, value=True)
regex_R1 = tkinter.Radiobutton(options_frame, text="Word/phrase", variable=is_regex, value=False)
regex_R2 = tkinter.Radiobutton(options_frame, text="Regular expression", variable=is_regex, value=True)

# Set up output type frame
output_type_frame = tkinter.Frame(all_content)
type_label = tkinter.Label(output_type_frame, text='Show search results as:')
output_type = tkinter.StringVar()
output_type.set('concordance')
output_R1 = tkinter.Radiobutton(output_type_frame, text="Concordance lines", variable=output_type, value='concordance', command=toggle_suboptions)
output_R2 = tkinter.Radiobutton(output_type_frame, text="Total frequency", variable=output_type, value='total frequency', command=toggle_suboptions)
output_R3 = tkinter.Radiobutton(output_type_frame, text="Frequency by category", variable=output_type, value='frequency by category', command=toggle_suboptions)
# Set up concordance suboption frame
context_len = tkinter.IntVar()
conc_option_frame = tkinter.Frame(output_type_frame)
context_len_menu = tkinter.Spinbox(conc_option_frame, from_=1.0, to=20, textvariable=context_len, width=2)
context_len_label = tkinter.Label(conc_option_frame, text='Number of context words: ')
# Set up category suboption frame
suboption_frame = tkinter.Frame(output_type_frame)
suboption_l1 = tkinter.Label(suboption_frame, text='Category:')
category = tkinter.StringVar()
category.set('writer')
category_R1 = tkinter.Radiobutton(suboption_frame, text="Writer", variable=category, value='writer')
category_R2 = tkinter.Radiobutton(suboption_frame, text="Recipient", variable=category, value='addressee')
category_R3 = tkinter.Radiobutton(suboption_frame, text="Year", variable=category, value='year')
suboption_l2 = tkinter.Label(suboption_frame, text='Frequency type:')
frequency_type = tkinter.StringVar()
frequency_type.set('raw')
frequency_R1 = tkinter.Radiobutton(suboption_frame, text="Raw", variable=frequency_type, value='raw')
frequency_R2 = tkinter.Radiobutton(suboption_frame, text="Normalized", variable=frequency_type, value='normalized')

# Set up file frame
file_frame = tkinter.Frame(all_content)
to_file = tkinter.BooleanVar()
to_file.set(False)
file_check = tkinter.Checkbutton(file_frame, text='Write to text file?', variable=to_file, onvalue=True, offvalue=False, command=toggle_file_entry)
filename = tkinter.StringVar()
file_entry = tkinter.Entry(file_frame, textvariable=filename)
file_label = tkinter.Label(file_frame, text='Enter the name of the file: ')

# Set up filter frame
filter_frame = tkinter.Frame(all_content)
# Set up writer filter
by_writer = tkinter.BooleanVar()
by_writer.set(False)
writer_check = tkinter.Checkbutton(filter_frame, text='Filter by writer', variable=by_writer, onvalue=True, offvalue=False, command=toggle_writer_filter)
writer_frame = tkinter.Frame(filter_frame)
with open('writers.pickle', 'rb') as wfin:
    writers = pickle.load(wfin)
writer_var = tkinter.StringVar(value=writers)
writer_filter = tkinter.Listbox(writer_frame, listvariable=writer_var, height=10, selectmode='extended')
writer_scroll = tkinter.Scrollbar(writer_frame, orient=tkinter.VERTICAL, command=writer_filter.yview)
writer_filter['yscrollcommand'] = writer_scroll.set
# Set up recipient filter
by_recipient = tkinter.BooleanVar()
by_recipient.set(False)
recipient_check = tkinter.Checkbutton(filter_frame, text='Filter by recipient', variable=by_recipient, onvalue=True, offvalue=False, command=toggle_recipient_filter)
recipient_frame = tkinter.Frame(filter_frame)
with open('addressees.pickle', 'rb') as afin:
    recipients = pickle.load(afin)
recipient_var = tkinter.StringVar(value=recipients)
recipient_filter = tkinter.Listbox(recipient_frame, listvariable=recipient_var, height=10, selectmode='extended')
recipient_scroll = tkinter.Scrollbar(recipient_frame, orient=tkinter.VERTICAL, command=recipient_filter.yview)
recipient_filter['yscrollcommand'] = recipient_scroll.set
# Set up year filter
by_year = tkinter.BooleanVar()
by_year.set(False)
year_check = tkinter.Checkbutton(filter_frame, text='Filter by Year', variable=by_year, onvalue=True, offvalue=False, command=toggle_year_filter)
year_frame = tkinter.Frame(filter_frame)
with open('years.pickle', 'rb') as yfin:
    years = pickle.load(yfin)
year_var = tkinter.StringVar(value=years)
year_filter = tkinter.Listbox(year_frame, listvariable=year_var, height=10, selectmode='extended')
year_scroll = tkinter.Scrollbar(year_frame, orient=tkinter.VERTICAL, command=year_filter.yview)
year_filter['yscrollcommand'] = year_scroll.set
# Set up language filter
lang_label = tkinter.Label(filter_frame, text='Filter by language')
lang_frame = tkinter.Frame(filter_frame)
language = tkinter.StringVar()
language.set('en')
lang_R1 = tkinter.Radiobutton(lang_frame, text="English", variable=language, value='en')
lang_R2 = tkinter.Radiobutton(lang_frame, text="French", variable=language, value='fr')

search_button = tkinter.Button(all_content, text='Search', command=search)

# Grid the major frames
all_content.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S), padx=10, pady=10)
root.columnconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
welcome.grid(column=0, row=0, padx=10, pady=10)
entry_frame.grid(column=0, row=1, padx=10, pady=10)
output_type_frame.grid(column=0, row=2, padx=10, pady=10)
file_frame.grid(column=0, row=3, padx=10, pady=10)
filter_frame.grid(column=0, row=4, padx=10, pady=10)
search_button.grid(column=0, row=5, padx=10, pady=10)

# Grid the widgets in the entry frame
entry_label.grid(column=0, row=0)
search_entry.grid(column=0, row=1)
options_frame.grid(column=0, row=2)
# Grid the widgets in the search options frame
options_label.grid(column=0, row=0, columnspan=2)
case_R1.grid(column=0, row=1, sticky=(tkinter.W), padx=1, pady=2)
case_R2.grid(column=0, row=2, sticky=(tkinter.W), padx=1, pady=2)
regex_R1.grid(column=1, row=1, sticky=(tkinter.W), padx=1, pady=2)
regex_R2.grid(column=1, row=2, sticky=(tkinter.W), padx=1, pady=2)

# Grid the widgets in the output type frame
type_label.grid(column=0, row=0, sticky=(tkinter.W))
output_R1.grid(column=0, row=1, sticky=(tkinter.W), padx=1, pady=2)
conc_option_frame.grid(column=0, row=2, sticky=(tkinter.W), padx=1, pady=2)
output_R2.grid(column=0, row=3, sticky=(tkinter.W), padx=1, pady=2)
output_R3.grid(column=0, row=4, sticky=(tkinter.W), padx=1, pady=2)
suboption_frame.grid(column=0, row=5)
# Grid the widgets in the concordance option frame
context_len_label.grid(column=0, row=0, sticky=(tkinter.W), padx=1, pady=2)
context_len_menu.grid(column=1, row=0, sticky=(tkinter.W), padx=1, pady=2)
# Grid the widgets in the category suboption frame
suboption_l1.grid(column=0, row=0, sticky=(tkinter.W), padx=1, pady=2)
suboption_l2.grid(column=1, row=0, sticky=(tkinter.W), padx=1, pady=2)
category_R1.grid(column=0, row=1, sticky=(tkinter.W), padx=1, pady=2)
category_R2.grid(column=0, row=2, sticky=(tkinter.W), padx=1, pady=2)
category_R3.grid(column=0, row=3, sticky=(tkinter.W), padx=1, pady=2)
frequency_R1.grid(column=1, row=1, sticky=(tkinter.W), padx=1, pady=2)
frequency_R2.grid(column=1, row=2, sticky=(tkinter.W), padx=1, pady=2)
# Hide suboption grid by default
suboption_frame.grid_remove()

# Grid the widgets in the file frame
file_check.grid(column=0, row=0, columnspan=2)
file_label.grid(column=0, row=1)
file_entry.grid(column=1, row=1)
# Hide entry box by default
file_label.grid_remove()
file_entry.grid_remove()

# Grid the widgets in the filter frame
writer_check.grid(column=0, row=0)
recipient_check.grid(column=1, row=0)
year_check.grid(column=2, row=0)
lang_label.grid(column=3, row=0)
writer_frame.grid(column=0, row=1, padx=2, pady=5)
recipient_frame.grid(column=1, row=1, padx=2, pady=5)
year_frame.grid(column=2, row=1, padx=2, pady=5)
lang_frame.grid(column=3, row=1, padx=2, pady=5, sticky=(tkinter.N, tkinter.S))
# Grid the widgets in the writer frame
writer_filter.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
writer_scroll.grid(column=1, row=0, sticky=(tkinter.N, tkinter.S))
# Grid the widgets in the recipient frame
recipient_filter.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
recipient_scroll.grid(column=1, row=0, sticky=(tkinter.N, tkinter.S))
# Grid the widgets in the year frame
year_filter.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
year_scroll.grid(column=1, row=0, sticky=(tkinter.N, tkinter.S))
# Grid the widgets in the language frame
lang_R1.grid(column=0, row=0, sticky=(tkinter.N))
lang_R2.grid(column=1, row=0, sticky=(tkinter.N))

# Hide filters by default
writer_frame.grid_remove()
recipient_frame.grid_remove()
year_frame.grid_remove()

root.mainloop()