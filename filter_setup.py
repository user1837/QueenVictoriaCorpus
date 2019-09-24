import pickle

# This module pickles lists of all writers, recipients, and years occurring in the Queen Victoria Correspondence Corpus to store them for the listboxes in the GUI

# These are the names as they will be displayed in the listbox
writers = ['Queen Victoria', 'Prince Albert', 'King of the Belgians', 'Mr Disraeli', 'Queen of the French', 'Earl of Malmesbury', 'Emperor of Austria', 'Colonel Phipps', 'Lord John Russell', 'Sir James Graham', 'Lord Fitzgerald', 'Duke of Newcastle', 'Marquis of Normanby', 'Princess Charlotte of Belgium', 'General Simpson', 'Lord Panmure', 'Lord Hill', 'Earl of Liverpool', 'General Grey' 'Earl of Clarendon', 'The Princess Royal', 'Lord Brougham', 'Adolphus Duke of Cambridge', 'Mr Delane', 'Queen Maria II of Portugal', 'King of Prussia', 'Duke of Wellington', 'Queen Adelaide', 'Duc de Nemours', 'Prince Edward of Saxe-Weimar', 'Sir Thomas Fremantle', 'King of Sardinia', 'Countess of Derby', 'Empress of the French', 'Earl Canning', 'Princess Hohenlohe', 'Emperor of the French', 'Duchess of Sutherland', 'Earl Cowley', 'Mr Featherstonhaugh', 'Duchess of Gloucester', 'Mr Leigh Hunt', 'Earl of Derby', 'Queen of the Belgians', 'Mr Labouchere', 'Earl of Aberdeen', 'Lord Stanley', 'Sir Francis Baring', 'King of Naples', 'Sir Robert Peel', 'Viscount Melbourne', 'Prince George of Cambridge', 'Mr Goulburn', 'Viscount Hardinge', 'Baron Stockmar', 'Prince of Prussia', 'Earl Granville', 'Earl Grey', 'Emperor of Russia', 'Lord Raglan', 'Viscount Palmerston', 'Earl of Ripon', 'Mr Bulwer', 'Mr Gladstone', 'Bishop of Oxford', 'Pope Pius IX', 'Marquis of Dalhousie', 'King of the French', 'Marchioness of Normanby', 'Mr Odo Russell', 'Lady Augusta Bruce', 'Duchess of Manchester', 'Lord Ellenborough', 'Sir E Bulwer Lytton', 'Duke of Buccleuch', 'Sir Charles Wood', 'King of Denmark']
writers.sort()
with open('writers.pickle', 'wb') as w_f:
    pickle.dump(writers, w_f)

addressees = ['Mr Disraeli', 'Queen of the French', 'Earl of Malmesbury', 'Emperor of Austria', 'Duchess of Kent', 'Colonel Phipps', 'Florence Nightingale', 'Mr Corbett', 'Lord John Russell', 'Sir James Graham', 'Duke of Newcastle', 'Duke of Sussex', 'General Simpson', 'Lord Chancellor', 'Duchess of Norfolk', 'Queen Victoria', 'Lord Panmure', 'Lord Hill', 'Mr Vernon Smith', 'Lady Raglan', 'Earl of Clarendon', 'King of Hanover', 'Sir William Codrington', 'Adolphus Duke of Cambridge', 'Sir John Pakington', 'General Peel', 'King of Prussia', 'Duke of Wellington', 'Queen Adelaide', 'Princess of Prussia', 'Empress of the French', 'Earl Canning', 'Emperor of the French', 'Duchess of Sutherland', 'Sir George Grey', 'Duchess of Gloucester', 'Earl of Derby', 'Queen of the Belgians', 'Viscountess Hardinge', 'Mr Labouchere', 'Earl of Aberdeen', 'Lord Stanley', 'Sir Francis Baring', 'Lord Lansdowne', 'Countess of Gainsborough', 'Sir Robert Peel', 'Viscount Melbourne', 'Prince George of Cambridge', 'Marchioness of Ely', 'King of Naples', 'Duke of Somerset', 'Viscount Hardinge', 'Baron Stockmar', 'Earl Granville', 'Earl Grey', 'Mr Anson', 'Emperor of Russia', 'Mr Walpole', 'King of the Belgians', 'Viscount Palmerston', 'Earl of Lincoln', 'Lord Raglan', 'Prince Albert', 'Earl Fitzwilliam', 'Mr Gladstone', 'Pope Pius IX', 'Marquis of Dalhousie', 'King of the French', 'Sir Charles Phipps', 'Lord Ellenborough', 'Sir E Bulwer Lytton', 'Sir Charles Wood', 'King of Denmark']
addressees.sort()
with open('addressees.pickle', 'wb') as a_f:
    pickle.dump(addressees, a_f)

years = ['1821', '1822', '1829', '1832', '1833', '1834', '1835', '1836', '1837', '1838', '1839', '1840', '1841', '1842', '1843', '1844', '1845', '1846', '1847', '1848', '1849', '1850', '1851', '1852', '1853', '1854', '1855', '1856', '1857', '1858', '1859', '1860', '1861', '1862']
with open('years.pickle', 'wb') as y_f:
    pickle.dump(years, y_f)



