'''
Description: 按钮状态事件
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-18 16:25:43
LastEditTime: 2022-04-24 15:16:58
'''

# -*- coding: utf-8 -*-
from hammerCookingScripts import logger


class NodeId(object):
    """node 状态与 ID
    """
    Idle = 1
    SelectSlot = 2
    UnSelectSlot = 3
    Swap = 4
    TouchProgressiveSelect = 5
    TouchProgressiveSelectComplete = 6
    TouchProgressiveSelectCancel = 7
    DropAll = 8
    Coalesce = 9


class ButtonEventType(object):
    """按钮事件
    """
    Clicked = 0
    Pressed = 1
    Released = 2
    DoubleClick = 3


class Node(object):
    """状态节点
    """
    def __init__(self, onEnter, onExit):
        """状态转移节点初始化

        Args:
            onEnter (func): 进入状态的函数
            onExit (func): 下一状态的函数
        """
        super(Node, self).__init__()
        self.mOnEnter = onEnter
        self.mOnExit = onExit

    def OnEnter(self, buttonPath):
        """执行进入状态

        Args:
            buttonPath (str): 按钮路径
        """
        if self.mOnEnter:
            self.mOnEnter(buttonPath)

    def OnExit(self, buttonPath):
        """执行下一状态

        Args:
            buttonPath (str): 按钮路径
        """
        if self.mOnExit:
            self.mOnExit(buttonPath)


class ButtonEdge(object):
    def __init__(self, target, requirement, priority):
        """状态转移条件

        Args:
            target (int): 下一状态 NodeId
            requirement (func)): 进入下一状态的函数
            priority (int): 优先级
        """
        super(ButtonEdge, self).__init__()
        self.mRequirement = requirement
        self.mTargetNodeId = target
        self.mPriority = priority

    def Requirement(self, buttonPath, buttonEventType):
        """状态转移函数

        Args:
            buttonPath (str): 按钮路径
            buttonEventType (int): ButtonEventType

        Returns:
            func: 执行状态转移函数，否则返回 False
        """
        if self.mRequirement:
            return self.mRequirement(buttonPath, buttonEventType)
        return False

    def GetTargetNodeId(self):
        """获取目标节点 ID

        Returns:
            int: NodeId
        """
        return self.mTargetNodeId

    def GetPriority(self):
        """获取优先级

        Returns:
            int: 优先级
        """
        return self.mPriority


class ContainerInteractionStateMachine(object):
    def __init__(self):
        super(ContainerInteractionStateMachine, self).__init__()
        self.mCurrentNode = None
        self.mCurrentNodeId = None
        self.mDefaultNodeId = NodeId.Idle
        self.mNodes = {}
        self.mButtonEdges = {}

    def AddNode(self, nodeId, onEnter=None, onExit=None, defaultNode=False):
        """加入状态节点

        Args:
            nodeId (int): NodeId 类型
            onEnter (func, optional): 进入该状态执行的函数. Defaults to None.
            onExit (func, optional): 离开该状态执行的函数. Defaults to None.
            defaultNode (boolean, optional): 是否为所有节点默认状态. Defaults to False.
        """
        if self.mNodes.get(nodeId) != None:
            logger.error(
                "{0} Node with the same name already exists in the state machine!"
                .format(nodeId))
            return
        node = Node(onEnter, onExit)
        self.mNodes[nodeId] = node
        self.mButtonEdges[nodeId] = []
        if defaultNode or self.mCurrentNodeId == None:
            self.mCurrentNode = node
            self.mCurrentNodeId = nodeId
            self.mDefaultNodeId = nodeId

    def AddEdge(self, source, target, requirement=None, priority=0):
        """加入状态转移条件

        Args:
            source (int): NodeId 类型
            target (int): NodeId 类型
            requirement (func, optional): 需要的条件, 返回 True/False. Defaults to None.
            priority (int, optional): 优先级. Defaults to 0.
        """
        edges = self.mButtonEdges.get(source)
        if not isinstance(edges, list):
            logger.error("there is no node named {0}".format(source))
            return
        targetIndex = -1
        for i in range(len(edges)):
            if edges[i].GetPriority() < priority:
                targetIndex = i
        if targetIndex == -1:
            edges.append(ButtonEdge(target, requirement, priority))
        else:
            edges.insert(targetIndex, ButtonEdge(target, requirement, priority))

    def ReceiveEvent(self, buttonPath, buttonEventType):
        """传入某一事件

        Args:
            buttonPath (str): 按钮路径
            buttonEventType (int): ButtonEventType
        """
        edges = self.mButtonEdges.get(self.mCurrentNodeId)
        if edges:
            for edge in edges:
                if edge.Requirement(buttonPath, buttonEventType):
                    self.ChangeState(edge.GetTargetNodeId(), buttonPath)
                    break

    def ResetToDefault(self):
        """回归默认状态
        """
        if self.mCurrentNodeId != self.mDefaultNodeId:
            self.ChangeState(self.mDefaultNodeId)

    def ChangeState(self, target, buttonPath=None):
        """改变状态

        Args:
            target (int): NodeId
            buttonPath (str, optional): 按钮路径. Defaults to None.
        """
        node = self.mNodes.get(target)
        if not node:
            logger.error("Tried to change to a nonexistant state!")
        self.mCurrentNode.OnExit(buttonPath)
        self.mCurrentNodeId = target
        self.mCurrentNode = self.mNodes[target]
        self.mCurrentNode.OnEnter(buttonPath)

    def GetCurrentNodeId(self):
        """获取已有的节点"""
        return self.mCurrentNodeId
