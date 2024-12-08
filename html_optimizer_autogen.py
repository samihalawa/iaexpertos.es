import os
import autogen
from typing import Dict, List, Tuple
import logging
from pathlib import Path
import shutil
from datetime import datetime

# Configure API settings
config_list = [
    {
        'api_key': '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',
        'api_base': 'https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct/v1',
        'model': 'Qwen/Qwen2.5-72B-Instruct'
    }
]

# Configure agents
assistant_config = {
    "seed": 42,
    "temperature": 0.7,
    "config_list": config_list,
    "timeout": 120,
}

class HTMLOptimizer:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.backup_file = f"{input_file}.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.logger = self._setup_logger()
        
        # Initialize Autogen agents
        self.structure_expert = autogen.AssistantAgent(
            name="StructureExpert",
            system_message="You are an expert in HTML structure and semantics. Your role is to analyze and suggest improvements to HTML structure, accessibility, and SEO.",
            llm_config=assistant_config,
        )
        
        self.style_expert = autogen.AssistantAgent(
            name="StyleExpert",
            system_message="You are an expert in modern CSS and visual design. Your role is to analyze and suggest improvements to styling, animations, and visual components.",
            llm_config=assistant_config,
        )
        
        self.coordinator = autogen.AssistantAgent(
            name="Coordinator",
            system_message="You are the optimization coordinator. Your role is to manage the optimization process and combine suggestions from other experts.",
            llm_config=assistant_config,
        )
        
        self.user_proxy = autogen.UserProxyAgent(
            name="UserProxy",
            system_message="You are coordinating the HTML optimization process.",
            human_input_mode="NEVER",
            code_execution_config={"work_dir": "web"},
        )

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("HTMLOptimizer")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def backup_original(self):
        """Create backup of original file"""
        shutil.copy2(self.input_file, self.backup_file)
        self.logger.info(f"Created backup at {self.backup_file}")

    def optimize(self):
        """Main optimization process using Autogen agents"""
        self.logger.info("Starting optimization process...")
        
        # Create backup
        self.backup_original()
        
        # Read original content
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Initialize the group chat
        groupchat = autogen.GroupChat(
            agents=[self.user_proxy, self.coordinator, self.structure_expert, self.style_expert],
            messages=[],
            max_round=5
        )
        manager = autogen.GroupChatManager(groupchat=groupchat)

        # Start the optimization chat
        self.user_proxy.initiate_chat(
            manager,
            message=f"""
            Please analyze and optimize this HTML content. Focus on:
            1. Semantic structure and accessibility
            2. Modern CSS practices and visual enhancements
            3. Performance optimizations
            
            HTML Content:
            {content}
            """
        )

        # Get the optimized content from the chat history
        chat_history = groupchat.messages
        optimized_content = self._extract_optimized_content(chat_history)
        
        # Add optimization metadata
        optimized_content = self._add_metadata(optimized_content)
        
        # Write optimized file
        with open(self.input_file, 'w', encoding='utf-8') as f:
            f.write(optimized_content)
            
        self.logger.info("Optimization complete!")

    def _extract_optimized_content(self, chat_history: List[Dict]) -> str:
        """Extract the optimized content from chat history"""
        # Find the last message containing optimized code
        for message in reversed(chat_history):
            if "```html" in message.get("content", ""):
                # Extract the HTML code between backticks
                content = message["content"]
                start = content.find("```html") + 7
                end = content.find("```", start)
                return content[start:end].strip()
        return ""

    def _add_metadata(self, content: str) -> str:
        """Add optimization metadata to HTML"""
        metadata = f"""
        <!-- 
        Optimized by HTML Optimizer using Autogen
        Date: {datetime.now().isoformat()}
        Agents: StructureExpert, StyleExpert, Coordinator
        -->
        """
        return metadata + content

def main():
    # Initialize optimizer
    optimizer = HTMLOptimizer("index.html")
    
    # Run optimization
    optimizer.optimize()

if __name__ == "__main__":
    main() 