# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from framework.translation import _

from framework.models import BaseModel

from .flink_job import *
from .paragraph import *
from .connector import Connector
from .project import *

