//
//  GameScene.swift
//  Checkers
//
//  Created by Michał Domański on 12/06/2020.
//  Copyright © 2020 Michał Domański. All rights reserved.
//

import SpriteKit
import GameplayKit

class GameScene: SKScene {
    
    private var label : SKLabelNode?
    private var spinnyNode : SKShapeNode?
    
    struct Checkerboard: Shape {
        let rows: Int
        let columns: Int
        
    }
    
    override func update(_ currentTime: TimeInterval) {
        // Called before each frame is rendered
    }
}
