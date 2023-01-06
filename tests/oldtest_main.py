import time
from telenium.tests import TeleniumTestCase


class NeodeemerTestCase(TeleniumTestCase):
    cmd_entrypoint = [u'main.py']
    
    def test_main(self):
        self.cli.send_keycode('ESCAPE')
        self.cli.send_keycode('ESCAPE')
        self.cli.wait_click('//MDTextField', timeout=2)
        self.assertTrue(self.cli.execute('app.artists_tab.ids.text_artists_search.text = 'Dymytry''))
        self.cli.send_keycode('ENTER')
        self.cli.wait_click('//ListLineArtist[0]', timeout=2)
        time.sleep(2)
        self.cli.wait_click('//ListLineAlbum[0]', timeout=2)
        time.sleep(5)
        self.cli.wait_click('//ListLineTrack[0]//IconRightWidget', timeout=2)
        self.cli.wait_click('//MDFillRoundFlatIconButton[2]', timeout=2)
        time.sleep(10)
        attr_name = 'title'
        attr_value = self.cli.getattr('//MDTopAppBar', attr_name)
        self.assertTrue(eval('title == 'Neodeemer - 1/1'', {attr_name: attr_value}))