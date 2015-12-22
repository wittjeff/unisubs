# Amara, universalsubtitles.org
#
# Copyright (C) 2015 Participatory Culture Foundation
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see
# http://www.gnu.org/licenses/agpl-3.0.html.

from contextlib import contextmanager
from datetime import datetime, timedelta
from django.test import TestCase
from nose.tools import *

from utils.test_utils import *
from utils.factories import *
from subtitles import pipeline
from videos.models import VideoIndex

class VideoIndexingTest(TestCase):
    @patch_for_test('videos.models.VideoIndex.calc_text')
    def test_index_new_video(self, mock_calc_text):
        mock_calc_text.return_value = 'test text'
        v = VideoFactory()
        assert_false(VideoIndex.objects.filter(video=v).exists())

        index = VideoIndex.index_video(v)
        assert_equal(VideoIndex.objects.get(video=v).text, 'test text')

    @patch_for_test('videos.models.VideoIndex.calc_text')
    def test_update_index(self, mock_calc_text):
        mock_calc_text.return_value = 'old text'
        v = VideoFactory()
        VideoIndex.index_video(v)

        mock_calc_text.return_value = 'new text'
        VideoIndex.index_video(v)
        assert_equal(VideoIndex.objects.get(video=v).text, 'new text')

    def test_index_text(self):
        video = VideoFactory(title='video_title',
                             description='video_description',
                             video_url__url='http://example.com/url_1')
        VideoURLFactory(video=video, url='http://example.com/url_2')
        pipeline.add_subtitles(video, 'en', [
            (0, 500, 'en_line1'),
            (1000, 1500, 'en_line2'),
        ], title='en_title', description='en_description', metadata={
            'speaker-name': 'en_speaker',
        }, visibility='public')
        pipeline.add_subtitles(video, 'fr', [
            (0, 500, 'fr_line1'),
            (1000, 1500, 'fr_line2'),
        ], title='fr_title', description='fr_description', metadata={
            'speaker-name': 'fr_speaker',
        }, visibility='public')
        # add a private tip, this text should not be included in the index
        pipeline.add_subtitles(video, 'es', [
            (0, 500, 'es_line1'),
            (1000, 1500, 'es_line2'),
        ], title='es_title', description='es_description', metadata={
            'speaker-name': 'es_speaker',
        }, visibility='private')

        index_text = VideoIndex.index_video(video).text
        assert_true('video_title' in index_text)
        assert_true('video_description' in index_text)
        assert_true('url_1' in index_text)
        assert_true('url_2' in index_text)
        assert_true('en_title' in index_text)
        assert_true('en_description' in index_text)
        assert_true('en_line1' in index_text)
        assert_true('en_line2' in index_text)
        assert_true('fr_title' in index_text)
        assert_true('fr_description' in index_text)
        assert_true('fr_line1' in index_text)
        assert_true('fr_line2' in index_text)
        assert_false('es_title' in index_text)
        assert_false('es_description' in index_text)
        assert_false('es_line1' in index_text)
        assert_false('es_line2' in index_text)

    # FIXME we should have searching tests, but we can't since we use sqlite
    # databases for our unittests and it has a different matching syntax then
    # MySQL