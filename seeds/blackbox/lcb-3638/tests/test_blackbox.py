import pytest
from solution import Solution


class TestMakeStringGood:
    """Tests for makeStringGood function."""

    def test_single_char(self):
        """Single character string - already good."""
        sol = Solution()
        assert sol.makeStringGood("a") == 0

    def test_two_same_chars(self):
        """Two identical characters - already good."""
        sol = Solution()
        assert sol.makeStringGood("aa") == 0

    def test_three_same_chars(self):
        """Three identical characters - already good."""
        sol = Solution()
        assert sol.makeStringGood("aaa") == 0

    def test_all_unique(self):
        """All unique characters - already good."""
        sol = Solution()
        assert sol.makeStringGood("abc") == 0

    def test_two_different(self):
        """Two different characters - already good."""
        sol = Solution()
        assert sol.makeStringGood("ab") == 0

    def test_aaa_b(self):
        """Three a's and one b - need 2 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaab") == 2

    def test_aabb(self):
        """Two a's and two b's - already good."""
        sol = Solution()
        assert sol.makeStringGood("aabb") == 0

    def test_aabbcc(self):
        """Three pairs - already good."""
        sol = Solution()
        assert sol.makeStringGood("aabbcc") == 0

    def test_aaa_bbb_cc(self):
        """Three of each - already good."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcc") == 0

    def test_aaabb(self):
        """Three a's, two b's - need 1 operation."""
        sol = Solution()
        assert sol.makeStringGood("aaabb") == 1

    def test_aab(self):
        """Two a's, one b - need 1 operation."""
        sol = Solution()
        assert sol.makeStringGood("aab") == 1

    def test_aaa_bbb_ccc_dd(self):
        """Three of a,b,c and two d's - need 1 operation."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccdd") == 1

    def test_aaa_bbb_ccc_ddd_ee(self):
        """Three of a,b,c,d and two e's - need 1 operation."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddde") == 1

    def test_aaa_bbb_ccc_ddd_eee(self):
        """Three of each - already good."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddd") == 0

    def test_aaa_bbb_ccc_ddd_eee_fff(self):
        """Three of each - already good."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefff") == 0

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg(self):
        """Three of each - already good."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggg") == 0

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhh(self):
        """Three of a-g, four h's - need 1 operation."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhh") == 1

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh(self):
        """Three of a-g, four h's - need 1 operation."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhh") == 1

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii(self):
        """Three of a-g, four h, i - need 2 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiii") == 2

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj(self):
        """Three of a-g, four h,i,j - need 3 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjj") == 3

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk(self):
        """Three of a-g, four h,i,j,k - need 4 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkk") == 4

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll(self):
        """Three of a-g, four h,i,j,k,l - need 5 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklll") == 5

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm(self):
        """Three of a-g, four h,i,j,k,l,m - need 6 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmm") == 6

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn(self):
        """Three of a-g, four h,i,j,k,l,m,n - need 7 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnn") == 7

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo(self):
        """Three of a-g, four h,i,j,k,l,m,n,o - need 8 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnooo") == 8

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo_ppp(self):
        """Three of a-g, four h,i,j,k,l,m,n,o,p - need 9 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnoooppp") == 9

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo_ppp_qqq(self):
        """Three of a-g, four h,i,j,k,l,m,n,o,p,q - need 10 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnooopppqqq") == 10

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo_ppp_qqq_rrr(self):
        """Three of a-g, four h,i,j,k,l,m,n,o,p,q,r - need 11 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnooopppqqqrrr") == 11

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo_ppp_qqq_rrr_sss(self):
        """Three of a-g, four h,i,j,k,l,m,n,o,p,q,r,s - need 12 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnooopppqqqrrrssss") == 12

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo_ppp_qqq_rrr_sss_ttt(self):
        """Three of a-g, four h,i,j,k,l,m,n,o,p,q,r,s,t - need 13 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnooopppqqqrrrssssttt") == 13

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo_ppp_qqq_rrr_sss_ttt_uuu(self):
        """Three of a-g, four h,i,j,k,l,m,n,o,p,q,r,s,t,u - need 14 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnooopppqqqrrrsssstttuuu") == 14

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo_ppp_qqq_rrr_sss_ttt_uuu_vvv(self):
        """Three of a-g, four h,i,j,k,l,m,n,o,p,q,r,s,t,u,v - need 15 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnooopppqqqrrrsssstttuuuvvv") == 15

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo_ppp_qqq_rrr_sss_ttt_uuu_vvv_www(self):
        """Three of a-g, four h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w - need 16 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnooopppqqqrrrsssstttuuuvvvwww") == 16

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo_ppp_qqq_rrr_sss_ttt_uuu_vvv_www_xxx(self):
        """Three of a-g, four h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x - need 17 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnooopppqqqrrrsssstttuuuvvvwwwxxx") == 17

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo_ppp_qqq_rrr_sss_ttt_uuu_vvv_www_xxx_yyy(self):
        """Three of a-g, four h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y - need 18 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnooopppqqqrrrsssstttuuuvvvwwwxxxxyyy") == 18

    def test_aaa_bbb_ccc_ddd_eee_fff_ggg_hhhh_iii_jjj_kkk_lll_mmm_nnn_ooo_ppp_qqq_rrr_sss_ttt_uuu_vvv_www_xxx_yyy_zzz(self):
        """Three of a-g, four h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z - need 19 operations."""
        sol = Solution()
        assert sol.makeStringGood("aaabbbcccddddeeefffggghhhhiijjjkkklllmmmnnooopppqqqrrrsssstttuuuvvvwwwxxxxyyyzzz") == 19

    def test_all_20k_chars_same(self):
        """All same characters - already good."""
        sol = Solution()
        s = "a" * 20000
        assert sol.makeStringGood(s) == 0

    def test_all_unique_26_chars(self):
        """All 26 unique characters - already good."""
        sol = Solution()
        assert sol.makeStringGood("abcdefghijklmnopqrstuvwxyz") == 0

    def test_20k_chars_all_different(self):
        """20k characters with same frequency - already good."""
        sol = Solution()
        s = "a" * 4000 + "b" * 4000 + "c" * 4000 + "d" * 4000 + "e" * 4000
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_two_frequencies(self):
        """20k characters with two different frequencies."""
        sol = Solution()
        s = "a" * 10000 + "b" * 10000
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_three_frequencies(self):
        """20k characters with three different frequencies."""
        sol = Solution()
        s = "a" * 6667 + "b" * 6667 + "c" * 6666
        assert sol.makeStringGood(s) == 1

    def test_20k_chars_four_frequencies(self):
        """20k characters with four different frequencies."""
        sol = Solution()
        s = "a" * 5000 + "b" * 5000 + "c" * 5000 + "d" * 5000
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_five_frequencies(self):
        """20k characters with five different frequencies."""
        sol = Solution()
        s = "a" * 4000 + "b" * 4000 + "c" * 4000 + "d" * 4000 + "e" * 4000
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_six_frequencies(self):
        """20k characters with six different frequencies."""
        sol = Solution()
        s = "a" * 3334 + "b" * 3334 + "c" * 3334 + "d" * 3334 + "e" * 3334 + "f" * 3334
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_seven_frequencies(self):
        """20k characters with seven different frequencies."""
        sol = Solution()
        s = "a" * 2857 + "b" * 2857 + "c" * 2857 + "d" * 2857 + "e" * 2857 + "f" * 2857 + "g" * 2857
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_eight_frequencies(self):
        """20k characters with eight different frequencies."""
        sol = Solution()
        s = "a" * 2500 + "b" * 2500 + "c" * 2500 + "d" * 2500 + "e" * 2500 + "f" * 2500 + "g" * 2500 + "h" * 2500
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_nine_frequencies(self):
        """20k characters with nine different frequencies."""
        sol = Solution()
        s = "a" * 2222 + "b" * 2222 + "c" * 2222 + "d" * 2222 + "e" * 2222 + "f" * 2222 + "g" * 2222 + "h" * 2222 + "i" * 2222
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_ten_frequencies(self):
        """20k characters with ten different frequencies."""
        sol = Solution()
        s = "a" * 2000 + "b" * 2000 + "c" * 2000 + "d" * 2000 + "e" * 2000 + "f" * 2000 + "g" * 2000 + "h" * 2000 + "i" * 2000 + "j" * 2000
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_eleven_frequencies(self):
        """20k characters with eleven different frequencies."""
        sol = Solution()
        s = "a" * 1818 + "b" * 1818 + "c" * 1818 + "d" * 1818 + "e" * 1818 + "f" * 1818 + "g" * 1818 + "h" * 1818 + "i" * 1818 + "j" * 1818 + "k" * 1818
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_twelve_frequencies(self):
        """20k characters with twelve different frequencies."""
        sol = Solution()
        s = "a" * 1667 + "b" * 1667 + "c" * 1667 + "d" * 1667 + "e" * 1667 + "f" * 1667 + "g" * 1667 + "h" * 1667 + "i" * 1667 + "j" * 1667 + "k" * 1667 + "l" * 1667
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_thirteen_frequencies(self):
        """20k characters with thirteen different frequencies."""
        sol = Solution()
        s = "a" * 1538 + "b" * 1538 + "c" * 1538 + "d" * 1538 + "e" * 1538 + "f" * 1538 + "g" * 1538 + "h" * 1538 + "i" * 1538 + "j" * 1538 + "k" * 1538 + "l" * 1538 + "m" * 1538
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_fourteen_frequencies(self):
        """20k characters with fourteen different frequencies."""
        sol = Solution()
        s = "a" * 1429 + "b" * 1429 + "c" * 1429 + "d" * 1429 + "e" * 1429 + "f" * 1429 + "g" * 1429 + "h" * 1429 + "i" * 1429 + "j" * 1429 + "k" * 1429 + "l" * 1429 + "m" * 1429 + "n" * 1429
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_fifteen_frequencies(self):
        """20k characters with fifteen different frequencies."""
        sol = Solution()
        s = "a" * 1334 + "b" * 1334 + "c" * 1334 + "d" * 1334 + "e" * 1334 + "f" * 1334 + "g" * 1334 + "h" * 1334 + "i" * 1334 + "j" * 1334 + "k" * 1334 + "l" * 1334 + "m" * 1334 + "n" * 1334 + "o" * 1334
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_sixteen_frequencies(self):
        """20k characters with sixteen different frequencies."""
        sol = Solution()
        s = "a" * 1250 + "b" * 1250 + "c" * 1250 + "d" * 1250 + "e" * 1250 + "f" * 1250 + "g" * 1250 + "h" * 1250 + "i" * 1250 + "j" * 1250 + "k" * 1250 + "l" * 1250 + "m" * 1250 + "n" * 1250 + "o" * 1250 + "p" * 1250
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_seventeen_frequencies(self):
        """20k characters with seventeen different frequencies."""
        sol = Solution()
        s = "a" * 1176 + "b" * 1176 + "c" * 1176 + "d" * 1176 + "e" * 1176 + "f" * 1176 + "g" * 1176 + "h" * 1176 + "i" * 1176 + "j" * 1176 + "k" * 1176 + "l" * 1176 + "m" * 1176 + "n" * 1176 + "o" * 1176 + "p" * 1176 + "q" * 1176
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_eighteen_frequencies(self):
        """20k characters with eighteen different frequencies."""
        sol = Solution()
        s = "a" * 1112 + "b" * 1112 + "c" * 1112 + "d" * 1112 + "e" * 1112 + "f" * 1112 + "g" * 1112 + "h" * 1112 + "i" * 1112 + "j" * 1112 + "k" * 1112 + "l" * 1112 + "m" * 1112 + "n" * 1112 + "o" * 1112 + "p" * 1112 + "q" * 1112 + "r" * 1112
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_nineteen_frequencies(self):
        """20k characters with nineteen different frequencies."""
        sol = Solution()
        s = "a" * 1053 + "b" * 1053 + "c" * 1053 + "d" * 1053 + "e" * 1053 + "f" * 1053 + "g" * 1053 + "h" * 1053 + "i" * 1053 + "j" * 1053 + "k" * 1053 + "l" * 1053 + "m" * 1053 + "n" * 1053 + "o" * 1053 + "p" * 1053 + "q" * 1053 + "r" * 1053 + "s" * 1053
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_twenty_frequencies(self):
        """20k characters with twenty different frequencies."""
        sol = Solution()
        s = "a" * 1000 + "b" * 1000 + "c" * 1000 + "d" * 1000 + "e" * 1000 + "f" * 1000 + "g" * 1000 + "h" * 1000 + "i" * 1000 + "j" * 1000 + "k" * 1000 + "l" * 1000 + "m" * 1000 + "n" * 1000 + "o" * 1000 + "p" * 1000 + "q" * 1000 + "r" * 1000 + "s" * 1000 + "t" * 1000
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_twentyone_frequencies(self):
        """20k characters with twenty-one different frequencies."""
        sol = Solution()
        s = "a" * 952 + "b" * 952 + "c" * 952 + "d" * 952 + "e" * 952 + "f" * 952 + "g" * 952 + "h" * 952 + "i" * 952 + "j" * 952 + "k" * 952 + "l" * 952 + "m" * 952 + "n" * 952 + "o" * 952 + "p" * 952 + "q" * 952 + "r" * 952 + "s" * 952 + "t" * 952 + "u" * 952
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_twentytwo_frequencies(self):
        """20k characters with twenty-two different frequencies."""
        sol = Solution()
        s = "a" * 909 + "b" * 909 + "c" * 909 + "d" * 909 + "e" * 909 + "f" * 909 + "g" * 909 + "h" * 909 + "i" * 909 + "j" * 909 + "k" * 909 + "l" * 909 + "m" * 909 + "n" * 909 + "o" * 909 + "p" * 909 + "q" * 909 + "r" * 909 + "s" * 909 + "t" * 909 + "u" * 909 + "v" * 909
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_twentythree_frequencies(self):
        """20k characters with twenty-three different frequencies."""
        sol = Solution()
        s = "a" * 870 + "b" * 870 + "c" * 870 + "d" * 870 + "e" * 870 + "f" * 870 + "g" * 870 + "h" * 870 + "i" * 870 + "j" * 870 + "k" * 870 + "l" * 870 + "m" * 870 + "n" * 870 + "o" * 870 + "p" * 870 + "q" * 870 + "r" * 870 + "s" * 870 + "t" * 870 + "u" * 870 + "v" * 870 + "w" * 870
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_twentyfour_frequencies(self):
        """20k characters with twenty-four different frequencies."""
        sol = Solution()
        s = "a" * 833 + "b" * 833 + "c" * 833 + "d" * 833 + "e" * 833 + "f" * 833 + "g" * 833 + "h" * 833 + "i" * 833 + "j" * 833 + "k" * 833 + "l" * 833 + "m" * 833 + "n" * 833 + "o" * 833 + "p" * 833 + "q" * 833 + "r" * 833 + "s" * 833 + "t" * 833 + "u" * 833 + "v" * 833 + "w" * 833 + "x" * 833
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_twentyfive_frequencies(self):
        """20k characters with twenty-five different frequencies."""
        sol = Solution()
        s = "a" * 800 + "b" * 800 + "c" * 800 + "d" * 800 + "e" * 800 + "f" * 800 + "g" * 800 + "h" * 800 + "i" * 800 + "j" * 800 + "k" * 800 + "l" * 800 + "m" * 800 + "n" * 800 + "o" * 800 + "p" * 800 + "q" * 800 + "r" * 800 + "s" * 800 + "t" * 800 + "u" * 800 + "v" * 800 + "w" * 800 + "x" * 800 + "y" * 800
        assert sol.makeStringGood(s) == 0

    def test_20k_chars_twenty_six_frequencies(self):
        """20k characters with twenty-six different frequencies."""
        sol = Solution()
        s = "a" * 769 + "b" * 769 + "c" * 769 + "d" * 769 + "e" * 769 + "f" * 769 + "g" * 769 + "h" * 769 + "i" * 769 + "j" * 769 + "k" * 769 + "l" * 769 + "m" * 769 + "n" * 769 + "o" * 769 + "p" * 769 + "q" * 769 + "r" * 769 + "s" * 769 + "t" * 769 + "u" * 769 + "v" * 769 + "w" * 769 + "x" * 769 + "y" * 769 + "z" * 769
        assert sol.makeStringGood(s) == 0
