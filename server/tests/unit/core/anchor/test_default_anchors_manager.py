from pytest import fixture, raises

from src.core.database.memory_kv_database import MemoryKVDatabase
from src.core.anchor.default_anchors_manager import DefaultAnchorsManager
from src.core.anchor.anchors_manager import AnchorAlreadyExistsException, UnknownAnchorException
from src.core.object.kvdb_static_objects_manager import KVDBStaticObjectsManager
from tests.unit.test_implementations.implementations import TestAnchor


class TestDefaultAnchorsManager:

    __ANCHOR_ID = "anchor_id"

    @fixture(autouse=True)
    def setUp(self):
        self.__test_anchor = TestAnchor(id=self.__ANCHOR_ID,
                                name="anchorName",
                                position=(0,0))
        self.__anchor_manager = DefaultAnchorsManager(KVDBStaticObjectsManager(MemoryKVDatabase()))

    def test_add_anchor(self):
        self.__anchor_manager.add_anchor(anchor_id=self.__ANCHOR_ID, anchor=self.__test_anchor)
        assert self.__anchor_manager.get_anchor(self.__ANCHOR_ID) == self.__test_anchor

    def test_add_anchor_with_same_id(self):
        self.__anchor_manager.add_anchor(anchor_id=self.__ANCHOR_ID, anchor=self.__test_anchor)
        sameIdAnchor = TestAnchor(id=self.__ANCHOR_ID,
                                name="otherAnchor",
                                position=(1,1))
        with raises(AnchorAlreadyExistsException):
            self.__anchor_manager.add_anchor(anchor_id=self.__ANCHOR_ID, anchor=sameIdAnchor)

    def test_add_multiple_anchors_and_get_all(self):
        all_anchors = [TestAnchor(id=str(anchorId), name="anchorName", position=(0,0)) for anchorId in range(100)]
        for anchor in all_anchors:
            self.__anchor_manager.add_anchor(anchor_id=anchor.id, anchor=anchor)
        retrieved_anchors = self.__anchor_manager.get_all_anchors()
        for anchor in all_anchors:
            assert anchor in retrieved_anchors

    def test_remove_anchor_and_try_get_it(self):
        self.__anchor_manager.add_anchor(anchor_id=self.__ANCHOR_ID, anchor=self.__test_anchor)
        assert self.__anchor_manager.get_anchor(self.__ANCHOR_ID) == self.__test_anchor
        self.__anchor_manager.remove_anchor(self.__ANCHOR_ID)
        with raises(UnknownAnchorException):
            self.__anchor_manager.get_anchor(anchor_id=self.__ANCHOR_ID)

    def test_get_anchor_from_empty_db(self):
        with raises(UnknownAnchorException):
            self.__anchor_manager.get_anchor(anchor_id=self.__ANCHOR_ID)

    def test_update_anchor(self):
        self.__anchor_manager.add_anchor(anchor_id=self.__ANCHOR_ID, anchor=self.__test_anchor)
        newAnchor = TestAnchor(id=self.__ANCHOR_ID,
                                name="newAnchorName",
                                position=(1,1))
        self.__anchor_manager.update_anchor(self.__ANCHOR_ID,
                                            newAnchor)
        assert self.__anchor_manager.get_anchor(anchor_id=self.__ANCHOR_ID) == newAnchor

    def test_update_not_existent_anchor(self):
        with raises(UnknownAnchorException):
            self.__anchor_manager.update_anchor(anchor_id="missingAnchorId", anchor={})