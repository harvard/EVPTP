

import csv, cPickle, sys
from create_dictionary_new import parse_new_date as parse_date


def main(treader, o2nf, n2of, osetf, nsetf):
    o2nd = {}
    n2od = {}
    oset = set()
    nset = set()

    l = treader.next()
    for l in treader:
        new_n = l[0]
        old_n = l[10]
        year, term = parse_date(l[2])
        old_n_d = ':'.join([old_n, year, term])
        n2od[new_n] = old_n_d
        o2nd[old_n_d] = new_n

        oset.add(old_n_d)
        nset.add(new_n)

    cPickle.dump(o2nd, o2nf)
    cPickle.dump(n2od, n2of)
    cPickle.dump(oset, osetf)
    cPickle.dump(nset, nsetf)
    return None



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python build_course_number_trans.py trans_file'
        print 'where trans_file contains the mapping from old numbers to new'
        sys.exit(1)
    t_file_name = sys.argv[1]
    t_reader = csv.reader(open(t_file_name, 'r'))
    o2n_file = open('old_2_new.dict', 'w')
    n2o_file = open('new_2_old.dict', 'w')
    o_set_file = open('old_num.set', 'w')
    n_set_file = open('new_num.set', 'w')
    main(t_reader, o2n_file, n2o_file, o_set_file, n_set_file)
